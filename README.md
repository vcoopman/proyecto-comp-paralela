Avance 1: proyecto semestral 
Introduccion a la Computacion Paralela 
=======================================
Topic: Optimización del Evaluator en el sistema de Log Detector

How to use it?

(1) Activate virtual env.

(2) python3 stress_test.py <docker_container_id> 
  This will save graphs into graphs folder.
  It will also start the docker_stats_fetcher process.
  
(3) Optional: Use docker_stats_fetcher/graph_maker.py to plot docker container stats during tests.
  python3 graph_maker.py -f <input_file> -s <start_date> -e <end_date>

