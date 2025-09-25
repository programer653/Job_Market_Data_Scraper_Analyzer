import pandas as pd 
from csv import writer
import re


def run_analyzer(job_title_filter):
    master_skill_list_1 = "python, java, javascript, typescript, c, c++, c#, ruby, go, rust, kotlin, swift, php, r, scala, julia, perl, matlab, dart, objectivec, vbnet, groovy, haskell, bash, powershell, pandas, numpy, scikit-learn, tensorflow, pytorch, keras, seaborn, matplotlib, statsmodels, nltk, spacy, opencv, xgboost, lightgbm, catboost, transformers, huggingface, langchain, mlflow, fastai, jax, prophet, gensim, word2vec, reinforcementlearning, deep learning, computer vision, nlp, data mining, feature engineering, sql, postgresql, mysql, sqlite, mongodb, cassandra, redis, dynamodb, snowflake, redshift, bigquery, oracle, db2, mariadb, neo4j, elasticsearch, firestore, cockroachdb, cosmosdb, hbase,spark, hadoop, hive, pig, flink, kafka, airflow, dbt, databricks, presto, trino, storm, aws glue, azure data factory, gcp dataflow, kafka streams, kudu, hdfs, beam, data lake,aws, gcp, azure, docker, kubernetes, terraform, ansible, jenkins, github actions, gitlab ci, circleci, travisci, helm, istio, consul, vault, promethus, grafana, cloudformation, ecs, ecr, lambda, sagemaker, cloudwatch, kinesis, react, react native, vue, angular, svelte, nextjs, gatsby, nodejs, express, django, flask, fastapi, springboot, ruby on rails, laravel, aspnet, tailwind, bootstrap, jquery, graphql, rest api, websocket, vite, webpack, babel, storybook, threejs, electron, capcitor, ionic, astro, git, github, gitlab, bitbucket, jira, confluence, slack, vscode, pycharm, intellij, eclipse, docker compose, postman, swagger, selenium, playwright, cypress, junit, pytest, unittest, mocha, chai, jest, npm, yarn, maven, gradle, linux, bash scripting, regex, agile, excel, tableau, power bi, qlik, looker, google data studio, sap, sas, spss, crystal reports, business intelligence, financial modeling, data visualization, a/b testing, hypothesis testing, statistics, probability, kpis, dashboards, reporting, data storytelling"
    master_skill_list = [s.strip() for s in master_skill_list_1.split(",")]
    df = pd.read_csv("./data/clean_jobs.csv") 

    #print(master_skill_list)
    
    df_filtered = df[df['job_title'].str.contains(job_title_filter, case=False, na=False)]
    with open(f'./data/skills_count_{job_title_filter}.csv', 'w', newline='', encoding='utf-8') as f:
            thewriter = writer(f)
            #count = 0
            heading = ['skill','count']
            thewriter.writerow(heading)
            for skill in master_skill_list:
                if skill.lower() in ["c++", "c#"]:
                    count = df_filtered['description'].str.contains(re.escape(skill), case=False, regex=True).sum()
                else:
                    pattern = rf"\b{re.escape(skill)}\b"
                    count = df_filtered['tokens'].str.contains(pattern, case=False, regex=True).sum()

                """skill_count = df['description'].apply(lambda x: True if ' '+skill+' ' in x else False)
                if skill_count is True:
                    count+=1"""
                thewriter.writerow([skill, count])
                print("skill: ", skill, "|count: ", count)

#run_analyzer(' ')