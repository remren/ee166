#!/bin/bash

# Usage: ./my_ez_script.sh [make_targets] [period]
# Examples:
#   ./my_ez_script.sh design_planning
#   ./my_ez_script.sh "place_opt clock_opt"  
#   ./my_ez_script.sh "clock_opt route_opt signoff" 1.5
#   ./my_ez_script.sh route_opt 2.0
#
# If no targets specified, runs all: design_planning place_opt clock_opt route_opt signoff

MAKE_TARGETS="${1:-design_planning place_opt clock_opt route_opt signoff}"
CLOCK_PERIOD="${2:-}"

# Activate virtual environment if not already activated
if [ -z "$VIRTUAL_ENV" ]; then
    if [ -f ".venv/bin/activate" ]; then
        echo "Activating virtual environment..."
        source .venv/bin/activate
        VIRTUAL_ENV_ACTIVATED=1
    else
        echo "Warning: .venv/bin/activate not found. Continuing without venv."
    fi
else
    echo "Virtual environment already active: $VIRTUAL_ENV"
fi

# Define the flow order for dependency checking
FLOW_STEPS=("design_planning" "place_opt" "clock_opt" "route_opt" "signoff")

# Function to validate make targets
validate_targets() {
    local targets=($1)
    local valid=true
    
    for target in "${targets[@]}"; do
        local found=false
        for valid_target in "${FLOW_STEPS[@]}"; do
            if [ "$target" = "$valid_target" ]; then
                found=true
                break
            fi
        done
        
        if [ "$found" = false ]; then
            echo "Error: Invalid make target '$target'"
            echo "Valid targets: ${FLOW_STEPS[*]}"
            valid=false
        fi
    done
    
    if [ "$valid" = false ]; then
        return 1
    fi
    
    # Check dependency order
    local highest_index=-1
    for target in "${targets[@]}"; do
        for i in "${!FLOW_STEPS[@]}"; do
            if [ "${FLOW_STEPS[$i]}" = "$target" ]; then
                if [ $i -lt $highest_index ]; then
                    echo "Error: Targets must be in flow order: ${FLOW_STEPS[*]}"
                    echo "You specified '$1' which has '$target' after a later step"
                    return 1
                fi
                highest_index=$i
                break
            fi
        done
    done
    
    return 0
}

# Validate the targets
if ! validate_targets "$MAKE_TARGETS"; then
    exit 1
fi

# Create results directory
RESULTS_DIR="backend_flow_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$RESULTS_DIR"

# Handle clock period modification if specified
if [ -n "$CLOCK_PERIOD" ]; then
    echo "Setting clock period to ${CLOCK_PERIOD}ns"
    
    cp scripts/tech.tcl scripts/tech.tcl.backup
    
    # Edit line 132 - preserve the semicolon and comment exactly
    sed -i "132s/set rm_clock_period [0-9.]*\(.*\)/set rm_clock_period $CLOCK_PERIOD\1/" scripts/tech.tcl
    
    echo "Modified line 132: $(sed -n '132p' scripts/tech.tcl)"
fi

echo "========================================="
echo "Starting backend flow execution"
echo "Steps to run: $MAKE_TARGETS"
echo "Results will be saved in: $RESULTS_DIR"
echo "========================================="

# Execute the make targets
MAKE_RESULT=0

echo ""
echo "Running: make $MAKE_TARGETS"
echo "----------------------------------------"

# Run all targets in a single make command with automatic exit detection
# Check if the make command spawns an interactive Innovus shell
if make $MAKE_TARGETS < <(echo "exit") 2>&1 | tee make_output.log; then
    echo "SUCCESS: All steps completed successfully"
    MAKE_RESULT=0
else
    # Check if we're stuck in an interactive shell
    if echo "$(tail -1 make_output.log)" | grep -q "innovus [0-9]*>"; then
        echo "Detected interactive Innovus shell, sending exit command..."
        # If make spawned an interactive shell, we need to handle it differently
        # This is a fallback - the primary method should work with the process substitution above
    fi
    echo "FAILED: Flow execution failed"
    MAKE_RESULT=1
fi

# Alternative approach: Run make with a timeout and auto-exit if stuck in Innovus
# Uncomment this section if the above method doesn't work
: '
{
    echo "make $MAKE_TARGETS"
    sleep 2  # Give make a moment to start
    # Monitor for Innovus prompt and send exit
    while true; do
        sleep 5
        if jobs -l | grep -q "make"; then
            # Check if Innovus prompt appeared
            echo "exit" > /proc/$(pgrep -f innovus)/fd/0 2>/dev/null || true
        else
            break
        fi
    done
} 2>&1 | tee make_output.log
'

# Save results regardless of success/failure
STATUS="success"
if [ $MAKE_RESULT -ne 0 ]; then
    STATUS="failed"
fi

# Create status-specific directory
RESULT_DIR="$RESULTS_DIR/flow_${STATUS}_$(date +%H%M%S)"
mkdir -p "$RESULT_DIR"

# Copy reports if they exist
if [ -d "reports" ]; then
    cp -r reports "$RESULT_DIR/"
fi

# Copy logs
for log in logs/*.log; do
    if [ -f "$log" ]; then
        cp "$log" "$RESULT_DIR/" 2>/dev/null
    fi
done

# Copy make output log if it exists
if [ -f "make_output.log" ]; then
    cp make_output.log "$RESULT_DIR/"
fi

# Copy work directory if needed
cp -r work "$RESULT_DIR/" 2>/dev/null

# Send Discord notification
if [ -f "discord_webhook_notif.py" ]; then
    if [ $MAKE_RESULT -eq 0 ]; then
        NOTIF_MSG="Backend flow ($MAKE_TARGETS): SUCCESS"
        [ -n "$CLOCK_PERIOD" ] && NOTIF_MSG="$NOTIF_MSG | Clock period: ${CLOCK_PERIOD}ns"
        python discord_webhook_notif.py "$NOTIF_MSG"
    else
        NOTIF_MSG="Backend flow ($MAKE_TARGETS): FAILED"
        [ -n "$CLOCK_PERIOD" ] && NOTIF_MSG="$NOTIF_MSG | Clock period: ${CLOCK_PERIOD}ns"
        python discord_webhook_notif.py "$NOTIF_MSG"
    fi
fi

# Clean up
if [ -f "scripts/tech.tcl.backup" ]; then
    rm scripts/tech.tcl.backup
fi
rm -f make_output.log

echo ""
echo "========================================="
echo "Flow Execution Complete!"
echo "Steps executed: $MAKE_TARGETS"
echo "Status: ${STATUS^^}"
echo "Results saved in: $RESULTS_DIR"
echo "========================================="

# Show results structure
echo ""
echo "Results structure:"
ls -la "$RESULTS_DIR"

# Deactivate venv if we activated it
if [ -n "$VIRTUAL_ENV_ACTIVATED" ] && [ "$VIRTUAL_ENV_ACTIVATED" = "1" ]; then
    deactivate 2>/dev/null
fi