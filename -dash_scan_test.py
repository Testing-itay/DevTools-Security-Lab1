import subprocess
import pickle
import hashlib
import yaml

# 1. Code injection (eval)
user_input = input()
result = eval(user_input)

# 2. Command injection (shell=True)
cmd = input("cmd: ")
subprocess.call(cmd, shell=True)

# 3. Insecure deserialization (pickle)
data = input("data: ").encode()
obj = pickle.loads(data)

# 4. Weak hash (md5)
digest = hashlib.md5(user_input.encode()).hexdigest()

# 5. Unsafe YAML load
config = yaml.load(user_input, Loader=yaml.Loader)

# 6. Hardcoded secret
API_KEY = "AKIAIOSFODNN7EXAMPLE"
PASSWORD = "hunter2-super-secret"
