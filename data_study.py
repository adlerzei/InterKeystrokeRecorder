# Copyright (C) 2020  Christian Zei
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from tasks import TaskGenerator as tasks
import config
import key_pair_generator as keygen

task_gen = tasks()
task_gen.welcome_task()
task_gen.task_1(config.key_pairs)
# task_gen.task_2(keygen.get_shift_pairs())
task_gen.task_3(config.words)
task_gen.task_4(config.passwords)
# task_gen.task_4(config.passwords, config.shift_passwords)
task_gen.task_5(config.random_passwords)
# task_gen.task_5(config.random_passwords, config.random_shift_passwords)
task_gen.goodbye_task()
