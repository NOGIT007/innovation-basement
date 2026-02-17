#!/bin/bash
# TeammateIdle hook — guide idle teammate to pick up next task
# Exit code 2 = send feedback to teammate (keeps them working)
# Exit code 0 = let teammate decide what to do

echo "Check TaskList for pending tasks with completed blockers. Claim and implement the next one. If no tasks remain, notify the lead that you are done."
exit 2
