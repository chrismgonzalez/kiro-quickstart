#!/bin/bash
set -e

# Demo Branch Checkpoint Script
# Save your current progress as a demo checkpoint branch

DEMO_PREFIX="demo"

# Checkpoint definitions
declare -A CHECKPOINTS=(
    ["00-start-here"]="Starting point - minimal CLI with test infrastructure"
    ["01-requirements"]="Initial requirements"
    ["02-design"]="First pass at the design"
    ["03-tasks"]="Sequenced tasks"
    ["04-test-first-red"]="Acceptance test written (RED - failing)"
    ["05-implementation"]="Implementation (GREEN - passing)"
    ["06-hooks-quality"]="Code quality hook"
    ["07-hooks-docs"]="Documentation synced with code"
)

# Ordered list for display
CHECKPOINT_ORDER=(
    "00-start-here"
    "01-requirements"
    "02-design"
    "03-tasks"
    "04-test-first-red"
    "05-implementation"
    "06-hooks-quality"
    "07-hooks-docs"
)

show_usage() {
    echo "🎬 Demo Branch Checkpoint Tool"
    echo ""
    echo "Usage:"
    echo "  $0 save <checkpoint>     Save current state as checkpoint"
    echo "  $0 list                  List all checkpoints"
    echo "  $0 goto <checkpoint>     Switch to a checkpoint"
    echo "  $0 delete <checkpoint>   Delete a checkpoint branch"
    echo "  $0 delete-all            Delete all demo branches"
    echo "  $0 push [checkpoint]     Push checkpoint(s) to remote"
    echo ""
    echo "Available checkpoints:"
    for cp in "${CHECKPOINT_ORDER[@]}"; do
        echo "  $cp - ${CHECKPOINTS[$cp]}"
    done
    echo ""
    echo "Examples:"
    echo "  $0 save 00-start-here              # Save current state"
    echo "  $0 goto 04-test-first-red          # Switch to checkpoint"
    echo "  $0 push 00-start-here              # Push one checkpoint"
    echo "  $0 push                            # Push all checkpoints"
}

check_git_repo() {
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        echo "❌ Error: Not in a git repository"
        exit 1
    fi
}

save_checkpoint() {
    local checkpoint=$1
    
    if [[ -z "${CHECKPOINTS[$checkpoint]}" ]]; then
        echo "❌ Error: Unknown checkpoint '$checkpoint'"
        echo "Run '$0 list' to see available checkpoints"
        exit 1
    fi
    
    local branch_name="$DEMO_PREFIX/$checkpoint"
    local description="${CHECKPOINTS[$checkpoint]}"
    
    # Check for uncommitted changes
    if ! git diff-index --quiet HEAD --; then
        echo "⚠️  You have uncommitted changes"
        read -p "Commit them now? (y/n) " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            git add -A
            git commit -m "Checkpoint: $checkpoint - $description"
        else
            echo "Please commit or stash changes first"
            exit 1
        fi
    fi
    
    # Check if branch already exists
    if git show-ref --verify --quiet "refs/heads/$branch_name"; then
        echo "⚠️  Branch '$branch_name' already exists"
        read -p "Overwrite it? (y/n) " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            git branch -D "$branch_name"
        else
            exit 0
        fi
    fi
    
    # Create branch from current HEAD
    git branch "$branch_name"
    
    echo "✅ Saved checkpoint: $branch_name"
    echo "   $description"
    echo ""
    echo "To switch to this checkpoint during demo:"
    echo "  git checkout $branch_name"
}

list_checkpoints() {
    echo "📋 Available Checkpoints:"
    echo ""
    
    for cp in "${CHECKPOINT_ORDER[@]}"; do
        local branch_name="$DEMO_PREFIX/$cp"
        local exists=""
        
        if git show-ref --verify --quiet "refs/heads/$branch_name"; then
            exists="✓"
        else
            exists=" "
        fi
        
        printf "  [%s] %s\n      %s\n\n" "$exists" "$cp" "${CHECKPOINTS[$cp]}"
    done
    
    echo "Legend: [✓] = saved, [ ] = not saved"
}

goto_checkpoint() {
    local checkpoint=$1
    
    if [[ -z "${CHECKPOINTS[$checkpoint]}" ]]; then
        echo "❌ Error: Unknown checkpoint '$checkpoint'"
        exit 1
    fi
    
    local branch_name="$DEMO_PREFIX/$checkpoint"
    
    if ! git show-ref --verify --quiet "refs/heads/$branch_name"; then
        echo "❌ Error: Checkpoint '$checkpoint' not saved yet"
        echo "Run '$0 save $checkpoint' first"
        exit 1
    fi
    
    # Check for uncommitted changes
    if ! git diff-index --quiet HEAD --; then
        echo "⚠️  You have uncommitted changes"
        read -p "Stash them? (y/n) " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            git stash
        else
            echo "Please commit or stash changes first"
            exit 1
        fi
    fi
    
    git checkout "$branch_name"
    echo "✅ Switched to checkpoint: $checkpoint"
}

delete_checkpoint() {
    local checkpoint=$1
    local branch_name="$DEMO_PREFIX/$checkpoint"
    
    if ! git show-ref --verify --quiet "refs/heads/$branch_name"; then
        echo "❌ Error: Checkpoint '$checkpoint' doesn't exist"
        exit 1
    fi
    
    git branch -D "$branch_name"
    echo "✅ Deleted checkpoint: $checkpoint"
}

delete_all() {
    echo "⚠️  This will delete ALL demo branches"
    read -p "Are you sure? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 0
    fi
    
    local deleted=0
    for cp in "${CHECKPOINT_ORDER[@]}"; do
        local branch_name="$DEMO_PREFIX/$cp"
        if git show-ref --verify --quiet "refs/heads/$branch_name"; then
            git branch -D "$branch_name"
            ((deleted++))
        fi
    done
    
    echo "✅ Deleted $deleted checkpoint branch(es)"
}

push_checkpoints() {
    local checkpoint=$1
    
    if [[ -n "$checkpoint" ]]; then
        # Push single checkpoint
        local branch_name="$DEMO_PREFIX/$checkpoint"
        if ! git show-ref --verify --quiet "refs/heads/$branch_name"; then
            echo "❌ Error: Checkpoint '$checkpoint' doesn't exist"
            exit 1
        fi
        git push -u origin "$branch_name"
        echo "✅ Pushed checkpoint: $checkpoint"
    else
        # Push all checkpoints
        local pushed=0
        for cp in "${CHECKPOINT_ORDER[@]}"; do
            local branch_name="$DEMO_PREFIX/$cp"
            if git show-ref --verify --quiet "refs/heads/$branch_name"; then
                git push -u origin "$branch_name"
                ((pushed++))
            fi
        done
        echo "✅ Pushed $pushed checkpoint branch(es)"
    fi
}

# Main script
check_git_repo

case "${1:-}" in
    save)
        if [[ -z "${2:-}" ]]; then
            echo "❌ Error: Checkpoint name required"
            echo "Run '$0 list' to see available checkpoints"
            exit 1
        fi
        save_checkpoint "$2"
        ;;
    list)
        list_checkpoints
        ;;
    goto)
        if [[ -z "${2:-}" ]]; then
            echo "❌ Error: Checkpoint name required"
            exit 1
        fi
        goto_checkpoint "$2"
        ;;
    delete)
        if [[ -z "${2:-}" ]]; then
            echo "❌ Error: Checkpoint name required"
            exit 1
        fi
        delete_checkpoint "$2"
        ;;
    delete-all)
        delete_all
        ;;
    push)
        push_checkpoints "${2:-}"
        ;;
    *)
        show_usage
        exit 1
        ;;
esac
