from tasks import TaskGenerator as tasks
import config

task_gen = tasks()
task_gen.welcome_task()
#task_gen.task_1()
#task_gen.task_2()
task_gen.task_3(config.words)
task_gen.task_4(config.passwords)
task_gen.task_5(config.random_passwords)

