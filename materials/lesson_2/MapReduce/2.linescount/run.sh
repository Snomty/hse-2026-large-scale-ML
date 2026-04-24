set -euo pipefail

rm -rf out

mapred streaming \
  -D mapreduce.job.reduces=1 \
  -input input.txt \
  -output out \
  -mapper "python3 mapper.py" \
  -reducer "python3 reducer.py" \
  -file mapper.py \
  -file reducer.py