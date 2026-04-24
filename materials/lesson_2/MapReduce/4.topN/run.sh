set -euo pipefail

rm -rf out1 out2

TOP_N=3

mapred streaming \
  -D mapreduce.job.reduces=2 \
  -input input.txt \
  -output out1 \
  -mapper "python3 pass1_mapper.py" \
  -reducer "python3 pass1_reducer.py" \
  -file pass1_mapper.py \
  -file pass1_reducer.py

mapred streaming \
  -D mapreduce.job.reduces=1 \
  -cmdenv TOP_N="$TOP_N" \
  -input out1 \
  -output out2 \
  -mapper "python3 pass2_mapper.py" \
  -reducer "python3 pass2_reducer.py" \
  -file pass2_mapper.py \
  -file pass2_reducer.py