# Step 3 Write up

## How did changing values on the SparkSession property parameters affect the throughput and latency of the data?

I ran Spark using localmode on a VirtualBox VM with 4GB RAM. The VM was running Ubuntu 18.04. Zookeeper and Kafka were
running locally on the VM along with Spark.

Changing the Spark configurations did appear to have some affect on the throughput and latency. Specifically there was
noticeable variation on the InputRowsPerSecond.

I only did 13 adhoc runs, so it was difficult to get a more consistent gauge of the performance differences. The performance
seemed to vary on multiple runs using the same parameters. See runs 2, 3, and 11.

I think it would be interesting to test out performance on a cluster with a bigger workload.


| Run | Key                                    | Value                                      | InputRowsPerSecond  | ProcessedRowsPerSecond |
| --- | ---------------------------------------| -------------------------------------------| -------------------:| ---------------------: |
| 1   | Defaults                               | Defaults                                   | 3.8593              | 15.0183                |
| 2   | spark.serializer                       | org.apache.spark.serializer.KryoSerializer | 8.6903              | 15.5231                |
| 3   | spark.serializer                       | org.apache.spark.serializer.KryoSerializer | 6.2476              | 15.1871                |
| 4   | spark.memory.fraction                  | 0.1                                        | 1.8731              | 13.7655                |
| 5   | spark.memory.fraction                  | 1.0                                        | 9.3274              | 13.5135                |
| 6   | spark.memory.storageFraction           | 0.1                                        | 2.1364              | 15.6592                |
| 7   | spark.memory.storageFraction           | 1.0                                        | 2.0694              | 14.3492                |
| 8   | spark.executor.memory                  | 1m                                         | ERROR               | ERROR                  |
| 9   | spark.executor.memory                  | 512m                                       | 1.6858              | 15.1297                |
| 10  | spark.python.worker.memory             | 128m                                       | 1.8207              | 15.3727                |
| 11  | spark.serializer                       | org.apache.spark.serializer.KryoSerializer | 3.6601              | 13.4652                |
| 12  | spark.serializer/spark.memory.fraction | KryoSerializer/1.0                         | 3.1567              | 14.2156                |
| 13  | spark.serializer/spark.memory.fraction | KryoSerializer/1.0                         | 7.8957              | 14.4634                |

## What were the 2-3 most efficient SparkSession property key/value pairs? Through testing multiple variations on values, how can you tell these were the most optimal?

It seemed using the `KryoSerializer` and increasing `spark.memory.fraction` led to the biggest performance boosts in terms of `InputRowsPerSecond`. The
`RowsProcessedPerSecond` value stayed fairly stable. It would be interesting to see how that would change if we increased `maxOffsetsPerTrigger` to a number
higher than `200`, such as `10000`.

With my limited testing I can't say that using `KryoSerializer` or increasing `spark.memory.fraction` are the optimal choice. Primarily I would need
to perform more test runs on each configuration to get a better sense of the typical performance. The noticeable variation in my test runs seems to say
that there may be some other factor I'm not aware of.

I do feel that using the `KyroSerializer` doesn't hurt.

In terms of `spark.memory.fraction`, I was surprised that this led to improved performance. The docs say to leave this at `0.6`. It doesn't make sense to
me that allocating 100% of memory for execution and storage would be an improvement.

# Installation

## Download Spark (2.4.4 with Hadoop 2.7)

- https://www.apache.org/dyn/closer.lua/spark/spark-2.4.4/spark-2.4.4-bin-hadoop2.7.tgz
- Unzip to repository `dev` folder

## Download Kafka (2.3.0 with Scala 2.11)

- https://kafka.apache.org/downloads
- Unzip to repository `dev` folder

## Start Vagrant

```
vagrant up
vagrant ssh
```

## Set up .bashrc

Add the following lines to the end of `/home/vagrant/.bashrc`

```
export SPARK_HOME=/vagrant/dev/spark-2.4.4-bin-hadoop2.7
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export PATH="$JAVA_HOME/bin:$SPARK_HOME/bin:/home/vagrant/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

## Install dependencies (JDK, Scala, PyEnv)

```
cd /vagrant
./set_up_workspace.sh
```

## Install pip requirements

Make sure that `which python` points to the python 3.7.2 installation.

If not, exit vagrant and ssh in again. This should update the path.

```
cd /vagrant
pip install -r src/requirements.txt
```
