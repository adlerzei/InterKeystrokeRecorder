from tasks import TaskGenerator as tasks
import config
import key_pair_generator as keygen

task_gen = tasks()
task_gen.welcome_task()
task_gen.task_1(config.key_pairs)
#task_gen.task_2(keygen.get_shift_pairs())
#task_gen.task_3(config.words)
task_gen.task_4(config.passwords)
task_gen.task_5(config.random_passwords)
task_gen.goodbye_task()