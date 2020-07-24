import commands
import os
import json

token = os.getenv('TOKEN')
commands.getstatusoutput('oc login https://kubernetes.default.svc.cluster.local --token={token}'.format())
data = commands.getstatusoutput('oc get cm -n namespace-configuration-operator group-labels -o json | jq -r ".data[]"')
groups = json.loads(data[1])
for group in groups:
  name = group["name"]
  oc=commands.getstatusoutput('oc get group {} -o name --ignore-not-found=true | cut -c 11-'.format(name))
  if oc[1]:
    labels = group["labels"]
    for label in labels:
      key = label["key"]
      value = label["value"]
      print('oc get group {} --template "{{{{ .metadata.labels.{} }}}}"'.format(name, key))
      oc=commands.getstatusoutput('oc get group {} --template "{{{{ .metadata.labels.{} }}}}"'.format(name, key))
      if "<no value>" in oc[1]:
        commands.getstatusoutput('oc label group {} {}={}'.format(name, key, value))