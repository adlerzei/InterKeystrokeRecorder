from tasks import TaskGenerator as tasks
import config

locale = ''

while True:
    locale = input("Please choose your desired language. Type G for German and E for English: ")
    locale = locale.casefold()
    if locale == 'g' or locale == 'e':
        break

if locale == 'g':
    import data_study_DE as lng
else:
    import data_study_EN as lng

print(lng.welcome_ascii)
print()
print(lng.welcome)
print()

task_gen = tasks(locale)
task_gen.task_1(config.chars)
task_gen.task_2(config.chars)
#task_gen.task_3(config.words)
#task_gen.task_4(config.passwords)


