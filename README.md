Introduccion a la Computacion Paralela - Proyecto Semestral 
==================================================================
Topic: Optimización del Evaluator en el sistema de Log Detector

How to use it?

(1) Activate virtual env.

(2) python3 stress_test.py <docker_container_id> 
  This will save graphs into graphs folder.
  It will also start the docker_stats_fetcher process.
  
(3) Optional: Use docker_stats_fetcher/graph_maker.py to plot docker container stats during tests.
  python3 graph_maker.py -f <input_file> -s <start_date> -e <end_date>

// ----------------------------------
// Avance 1
// ----------------------------------


// ----------------------------------
// Avance 2
// ----------------------------------


// ----------------------------------
// Avance 3 - Final
// ----------------------------------

TO DO:
 - Test with different frameworks (falco, japronto, fastapi, flask). [  ]
 - Test with different amount of gunicorn workers (from a bit less that CPUs x 2 + 1 until perfomance degradence). Hablar y explicar sobre como funciona gunicorn [  ]
 - Informe. [  ]
 - Presentación. [  ] (Presentar conclusiones reales de que se usaria)
 
DONE:
 - Implementent stress_test.py using subprocess. [  ]  (Won't do, because we already reach high % of cpu usage. Not needed)
 - Fix test setting to only introduce changes on one axis. [x]
 
 
 
Settings:

clients/logs | 200 | 400 | 600 | 800 | 1000 | 1200
--------------------------------------------------------
      3      |
      4      |
      6      |
      8      |
      10     |
      12     |
