# Benchmark performance

## HW specification

- CPU: i5-8400 @ 2.80GHz
- RAM: 16GB 2400Mhz

## Keyword sanitization

| db | benchmark | number of properties | distinct values | time |
| --- | --- | --- | --- | --- |
| patientv5 | brutal_delete | 237878 | # | 43.89s |
| patientv5 | faker | 237878 | # | 2122.07s |
| patientv5 | encrypt | 237878 | 52978 | 2573.47s |

| db | benchmark | number of properties | distinct values | time |
| --- | --- | --- | --- | --- |
| patientv5 | encrypt_extended | 738684 | 106851 | 18597.24s |
| patientv5 | encrypt | 237878 | 52978 | 2573.47s |
| patientv5 | encrypt_reduced | 113823 | 27383 | 741.21s |
| patientv5 | encrypt_minimal | 52364 | 19803 | 336.27s |

| db | benchmark | number of properties | distinct values | time |
| --- | --- | --- | --- | --- |
| patientv5_duplicated | encrypt | 414297 | 52978 | 3975.57s |
| patientv5 | encrypt | 237878 | 52978 | 2573.47s |

## NER sanitization

| db | sanitization | distinct values | NER utilization | NER models | time | average CPU usage |
| --- | --- | --- | --- | ---- | --- | --- |
| patientv5 after brutal_delete | ner_singleprocessing_suppression | 126350 | 367020 | 3 |  1964.91 s | 26% |
| patientv5 after brutal_delete | ner_multiprocessing_suppression | 126350 | 367020 | 3 |  922.66 s | 66% |
| patientv5 after brutal_delete | ner_multiprocessing_encrypt | 126350 | 367020 | 3 |  940.15 s | 66% |
| patientv5 after brutal_delete | ner_multiprocessing_anonomize | 126350 | 367020 | 3 |  919.15 s | 66% |
| patientv5 after brutal_delete | ner_multiprocessing_faker | 126350 | 367020 | 3 |  914.66 s | 66% |

| db | sanitization | distinct values | NER utilization | NER models | time | average CPU usage |
| --- | --- | --- | --- | ---- | --- | --- |
| patientv5 after brutal_delete | ner_multiprocessing_suppression | 126350 | 367020 | 3 |  922.66 s | 66% |
| patientv5 after brutal_delete | ner_suppression_extendedv1 | 180223 | 528639 | 3 |  1221.78 s | 66% |
| patientv5 after brutal_delete | ner_suppression_extendedv2 | 249289 | 735795 | 3 |  2459.94 s | 66% |
