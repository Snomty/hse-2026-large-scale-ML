#!/usr/bin/env bash
set -euo pipefail

rm -rf out

STREAMING_JAR="$HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.4.2.jar"

hadoop jar "$STREAMING_JAR" \
  -D stream.num.map.output.key.fields=2 \
  -D mapreduce.map.output.key.field.separator=$'\t' \
  -D mapreduce.partition.keypartitioner.options="-k1,1" \
  -D mapreduce.job.output.key.comparator.class=org.apache.hadoop.mapreduce.lib.partition.KeyFieldBasedComparator \
  -D mapreduce.partition.keycomparator.options="-k1,1 -k2,2" \
  -D mapreduce.job.reduces=2 \
  -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
  -input input.txt \
  -output out \
  -mapper "python3 mapper.py" \
  -reducer "python3 reducer.py" \
  -file mapper.py -file reducer.py