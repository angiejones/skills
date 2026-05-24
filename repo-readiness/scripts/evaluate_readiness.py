#!/usr/bin/env python3
"""
Deterministic repository readiness evaluator for AI-assisted development.

Checks for signals that indicate a repository is well-structured for AI collaboration:
- Agent context files (AGENTS.md, CLAUDE.md)
- Agent rules (copilot-instructions.md, prompts/)
- Repeatable workflows (SKILL.md, recipe.yaml files)
- Signal quality and maturity

Outputs JSON to stdout with score, level, signals, and recommendations.
"""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Dict, List, Tuple
import re


def get_repo_root() -> Path:
    """Get the repository root directory (current working directory)."""
    return Path.cwd()


def resolve_repo_root(target: str = None) -> Tuple[Path, tempfile.TemporaryDirectory]:
    """Resolve a local path or owner/repo target to a repository root."""
    if not target:
        return Path.cwd(), None

    expanded = Path(target).expanduser()
    if target.startswith(('/', './', '../', '~')) or expanded.exists():
        return expanded.resolve(), None

    if re.fullmatch(r'[^/\s]+/[^/\s]+', target):
        temp_dir = tempfile.TemporaryDirectory()
        clone_path = Path(temp_dir.name) / target.split('/')[1]
        subprocess.run(
            ['git', 'clone', '--depth', '1', f'https://github.com/{target}.git', str(clone_path)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return clone_path, temp_dir

    raise ValueError(f"Unsupported target '{target}'. Use a local path or owner/repo.")


def file_exists_and_readable(repo_root: Path, filepath: str) -> bool:
    """Check if a file exists and is readable."""
    try:
        full_path = repo_root / filepath
        return full_path.exists() and full_path.is_file()
    except (OSError, ValueError):
        return False


def find_files_matching(repo_root: Path, pattern: str, max_depth: int = 10) -> List[str]:
    """Find files matching a pattern (e.g., '**/*.md' or '**/SKILL.md')."""
    try:
        matches = []
        for path in repo_root.glob(pattern):
            if path.is_file():
                try:
                    rel_path = path.relative_to(repo_root)
                    matches.append(str(rel_path))
                except ValueError:
                    pass
        return matches
    except (OSError, ValueError):
        return []


def file_has_content(repo_root: Path, filepath: str, min_chars: int = 100) -> bool:
    """Check if a file has meaningful content (not just boilerplate)."""
    try:
        full_path = repo_root / filepath
        if not full_path.exists():
            return False
        content = full_path.read_text(encoding='utf-8', errors='ignore')
        # Remove comments and whitespace
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        meaningful_lines = [l for l in lines if not l.startswith('#')]
        return len(content) >= min_chars and len(meaningful_lines) > 0
    except (OSError, IOError):
        return False


def count_directory_instructions(repo_root: Path) -> Tuple[int, List[str]]:
    """Count .instructions.md files in the repository."""
    instructions = find_files_matching(repo_root, '**/.instructions.md')
    return len(instructions), instructions


def count_skill_files(repo_root: Path) -> Tuple[int, List[str]]:
    """Count SKILL.md files in the repository."""
    skills = find_files_matching(repo_root, '**/SKILL.md')
    return len(skills), skills


def count_recipe_files(repo_root: Path) -> Tuple[int, List[str]]:
    """Count recipe.yaml files in the repository."""
    recipes = find_files_matching(repo_root, '**/recipe.yaml')
    return len(recipes), recipes


def has_prompts_directory(repo_root: Path) -> Tuple[bool, int]:
    """Check if a prompts/ directory exists and has content."""
    prompts_dir = repo_root / 'prompts'
    if not prompts_dir.exists() or not prompts_dir.is_dir():
        return False, 0
    
    # Count prompt files
    count = 0
    try:
        for item in prompts_dir.iterdir():
            if item.is_file():
                count += 1
    except OSError:
        pass
    
    return count > 0, count


def evaluate_agents_file(repo_root: Path, filename: str) -> Tuple[int, str]:
    """
    Evaluate the quality of an AGENTS.md or CLAUDE.md file.
    
    Returns: (points, description)
    """
    if not file_exists_and_readable(repo_root, filename):
        return 0, f"{filename} not found"
    
    if not file_has_content(repo_root, filename, min_chars=200):
        return 5, f"{filename} exists but too minimal"
    
    try:
        path = repo_root / filename
        content = path.read_text(encoding='utf-8', errors='ignore').lower()
        
        # Good structure indicators
        has_sections = '##' in content or '###' in content
        has_structure = bool(content) and len(content) > 500
        
        if has_sections and has_structure:
            return 18, f"{filename} is well-structured"
        elif has_structure:
            return 15, f"{filename} exists with good content"
        else:
            return 10, f"{filename} exists but needs more detail"
    except (OSError, IOError):
        return 5, f"{filename} exists but unreadable"


def evaluate_copilot_instructions(repo_root: Path) -> Tuple[int, List[str]]:
    """Evaluate copilot-instructions.md quality anywhere in the repository."""
    files = find_files_matching(repo_root, '**/copilot-instructions.md')
    if not files:
        return 0, []

    filepath = files[0]
    if not file_has_content(repo_root, filepath, min_chars=150):
        return 5, files
    
    try:
        path = repo_root / filepath
        content = path.read_text(encoding='utf-8', errors='ignore').lower()
        
        # Check for quality indicators
        has_sections = '##' in content
        has_rules = any(keyword in content for keyword in ['must', 'should not', 'avoid', 'constraint', 'rule'])
        has_examples = '```' in content or 'example' in content
        
        score = 10  # base for existing
        if has_sections:
            score += 5
        if has_rules:
            score += 8
        if has_examples:
            score += 7
        
        return min(30, score), files
    except (OSError, IOError):
        return 5, files


def evaluate_signal_maturity(repo_root: Path, context_filename: str = None) -> int:
    """Evaluate overall maturity of signals (quality, completeness, maintenance)."""
    score = 0
    
    # Check for signal presence (basic heuristic)
    recent_count = 0
    try:
        if context_filename and (repo_root / context_filename).exists():
            recent_count += 1
        elif not context_filename:
            if (repo_root / 'AGENTS.md').exists() or (repo_root / 'CLAUDE.md').exists():
                recent_count += 1

        if find_files_matching(repo_root, '**/copilot-instructions.md'):
            recent_count += 1
        if find_files_matching(repo_root, '**/SKILL.md') or find_files_matching(repo_root, '**/recipe.yaml'):
            recent_count += 1
    except (OSError, ValueError):
        pass
    
    # Maturity scoring
    if recent_count >= 4:
        score = 18
    elif recent_count >= 3:
        score = 14
    elif recent_count >= 2:
        score = 10
    elif recent_count >= 1:
        score = 6
    else:
        score = 0
    
    return score


def calculate_recommendations(signals_found: Dict) -> List[Dict]:
    """Generate prioritized recommendations based on what's missing."""
    recommendations = []
    
    # Score each signal to determine impact
    signal_scores = {}
    
    if signals_found['agent_context']['points'] == 0:
        signal_scores['AGENTS.md or CLAUDE.md'] = (20, 'HIGH', 
            'Foundation for all AI context. AGENTS.md is preferred, but CLAUDE.md is accepted as a fallback.')
    
    if signals_found['agent_rules']['points'] == 0:
        signal_scores['agent rules'] = (30, 'HIGH',
            'Rules and constraints for AI. Add copilot-instructions.md or a prompts/ directory.')
    
    # Either SKILL.md or recipe.yaml can satisfy repeatable workflow guidance.
    if (
        signals_found['workflows']['skill_files']['points'] == 0
        and signals_found['workflows']['recipe_files']['points'] == 0
    ):
        signal_scores['repeatable workflows'] = (30, 'MEDIUM',
            'Documented repeatable workflows. Add SKILL.md files or recipe.yaml files.')
    
    # Sort by impact and create recommendations
    sorted_signals = sorted(signal_scores.items(), key=lambda x: x[1][0], reverse=True)
    
    for idx, (signal_name, (points, impact_level, description)) in enumerate(sorted_signals, 1):
        recommendations.append({
            'rank': idx,
            'signal': signal_name,
            'impact_level': impact_level,
            'potential_points': points,
            'why': description
        })
    
    return recommendations


def evaluate_repository(repo_root: Path) -> Dict:
    """
    Perform complete repository readiness evaluation.
    
    Returns a dictionary with score, level, signals found, and recommendations.
    """
    
    # AGENT CONTEXT EVALUATION (20 points)
    # AGENTS.md is preferred. If present, evaluate only AGENTS.md and ignore CLAUDE.md.
    # CLAUDE.md is accepted only as a fallback for repos that do not use AGENTS.md.
    agents_score, agents_desc = evaluate_agents_file(repo_root, 'AGENTS.md')
    if file_exists_and_readable(repo_root, 'AGENTS.md'):
        context_filename = 'AGENTS.md'
        context_score = agents_score
        context_desc = agents_desc
        claude_score, claude_desc = 0, 'Ignored because AGENTS.md is present'
    else:
        claude_score, claude_desc = evaluate_agents_file(repo_root, 'CLAUDE.md')
        context_filename = 'CLAUDE.md' if file_exists_and_readable(repo_root, 'CLAUDE.md') else None
        context_score = claude_score
        context_desc = claude_desc
    
    # AGENT RULES EVALUATION (30 points)
    copilot_instructions_score, copilot_instructions_files = evaluate_copilot_instructions(repo_root)
    
    instructions_count, instructions_files = count_directory_instructions(repo_root)
    instructions_score = min(10, instructions_count * 2 + (5 if instructions_count > 0 else 0))
    
    prompts_exists, prompts_count = has_prompts_directory(repo_root)
    prompts_score = min(5, 3 + (2 if prompts_count >= 3 else 0)) if prompts_exists else 0
    
    rules_score = max(copilot_instructions_score, 30 if instructions_score > 0 else 0, 30 if prompts_score > 0 else 0)
    
    # WORKFLOWS EVALUATION (30 points)
    # SKILL.md files and recipe.yaml files are interchangeable workflow signals.
    skills_count, skills_files = count_skill_files(repo_root)
    skills_score = min(30, skills_count * 3 + (5 if skills_count > 0 else 0))
    
    recipe_count, recipe_files = count_recipe_files(repo_root)
    recipe_score = min(30, recipe_count * 3 + (5 if recipe_count > 0 else 0))
    
    workflows_score = max(skills_score, recipe_score)
    
    # SIGNAL MATURITY EVALUATION (20 points)
    maturity_score = evaluate_signal_maturity(repo_root, context_filename)
    maturity_score = min(20, maturity_score)
    
    # TOTAL SCORE
    total_score = context_score + rules_score + workflows_score + maturity_score
    
    # Determine level
    if total_score >= 90:
        level = "Optimized"
    elif total_score >= 70:
        level = "Advanced"
    elif total_score >= 50:
        level = "Developing"
    elif total_score >= 25:
        level = "Minimal"
    else:
        level = "Not Ready"
    
    # Build signals found structure
    signals_found = {
        'agent_context': {
            'selected_file': context_filename,
            'points': context_score,
            'description': context_desc,
            'files': [context_filename] if context_filename else [],
            'agents_md': {'points': agents_score if context_filename == 'AGENTS.md' else 0, 'description': agents_desc if context_filename == 'AGENTS.md' else 'AGENTS.md not found', 'files': ['AGENTS.md'] if context_filename == 'AGENTS.md' else []},
            'claude_md': {'points': claude_score if context_filename == 'CLAUDE.md' else 0, 'description': claude_desc if context_filename == 'CLAUDE.md' else 'CLAUDE.md not evaluated' if context_filename == 'AGENTS.md' else 'CLAUDE.md not found', 'files': ['CLAUDE.md'] if context_filename == 'CLAUDE.md' else []},
        },
        'agent_rules': {
            'points': rules_score,
            'copilot_instructions': {'points': copilot_instructions_score, 'description': f'{len(copilot_instructions_files)} copilot-instructions.md files', 'files': copilot_instructions_files},
            'instructions_files': {'points': 30 if instructions_score > 0 else 0, 'description': f'{instructions_count} .instructions.md files', 'files': instructions_files},
            'prompts_directory': {'points': 30 if prompts_score > 0 else 0, 'description': f'prompts/ with {prompts_count} files', 'files': [] if prompts_exists else []},
        },
        'workflows': {
            'skill_files': {'points': skills_score, 'description': f'{skills_count} SKILL.md files', 'files': skills_files},
            'recipe_files': {'points': recipe_score, 'description': f'{recipe_count} recipe.yaml files', 'files': recipe_files},
        },
        'maturity': {
            'signal_quality': {'points': maturity_score, 'description': 'Overall signal quality and maintenance', 'files': []},
        }
    }
    
    # Generate recommendations
    recommendations = calculate_recommendations(signals_found)
    
    return {
        'score': total_score,
        'max_score': 100,
        'level': level,
        'scoring_breakdown': {
            'agent_context': context_score,
            'agent_rules': rules_score,
            'workflows': workflows_score,
            'maturity': maturity_score,
        },
        'signals_found': signals_found,
        'recommendations': recommendations,
        'reasoning': f"Repository readiness is {level.lower()}. Focus on the top recommendations to improve AI-assisted development."
    }


def main():
    """Main entry point."""
    temp_dir = None
    try:
        target = sys.argv[1] if len(sys.argv) > 1 else None
        repo_root, temp_dir = resolve_repo_root(target)
        result = evaluate_repository(repo_root)
        result['target'] = target or str(repo_root)
        result['repo_root'] = str(repo_root)
        print(json.dumps(result, indent=2))
        return 0
    except Exception as e:
        error_result = {
            'error': str(e),
            'score': 0,
            'level': 'Error'
        }
        print(json.dumps(error_result, indent=2), file=sys.stderr)
        return 1
    finally:
        if temp_dir:
            temp_dir.cleanup()


if __name__ == '__main__':
    sys.exit(main())
