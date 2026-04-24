set -euo pipefail

rm -rf out

mapred streaming \
  -D mapreduce.job.reduces=2 \
  -input users.tsv \
  -input events.tsv \
  -output out \
  -mapper "python3 mapper.py" \
  -reducer "python3 reducer.py" \
  -file mapper.py \
  -file reducer.py