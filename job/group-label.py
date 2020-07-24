import subprocess
import os
import json

def bash_command_pipe(cmd): 
    ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    return ps.communicate()[0]

def bash_command(cmd): 
    return subprocess.check_output(cmd)

token = os.getenv('TOKEN')
bash_command('oc login https://kubernetes.default.svc.cluster.local --token={}'.format(token))
data = bash_command_pipe('oc get cm -n namespace-configuration-operator group-labels -o json | jq -r ".data[]"')
groups = json.loads(data[1])
for group in groups:
  name = group["name"]
  oc=bash_command_pipe('oc get group {} -o name --ignore-not-found=true | cut -c 11-'.format(name))
  if oc[1]:
    labels = group["labels"]
    for label in labels:
      key = label["key"]
      value = label["value"]
      print('oc get group {} --template "{{{{ .metadata.labels.{} }}}}"'.format(name, key))
      oc=bash_command('oc get group {} --template "{{{{ .metadata.labels.{} }}}}"'.format(name, key))
      if "<no value>" in oc[1]:
        bash_command('oc label group {} {}={}'.format(name, key, value))