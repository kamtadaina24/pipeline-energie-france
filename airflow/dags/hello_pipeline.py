from airflow.sdk import dag, task


@dag(schedule=None)
def hello_pipeline():
    @task
    def etape_a():
        print("Etape A terminee")

    @task
    def etape_b():
        print("Etape B terminee")

    a = etape_a()
    b = etape_b()
    a >> b


hello_pipeline()