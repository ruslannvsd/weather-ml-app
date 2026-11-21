# weather-ml-app
GCU DevOps Coursework 2

## Operations · CW2 Task 3

Run these commands from the repository root **on the x86-64 Ubuntu Production Server**, signed in as the regular sudo user. The playbook installs Docker if needed, grants that user Docker access, installs checksum-verified kubectl and Minikube, and deploys two replicas of the published v1 image. Docker group membership gives the account root-equivalent access. The Minikube node uses two CPUs and 3 GiB of memory. Check available disk space before downloading images.

```bash
sudo apt-get update
sudo apt-get install -y ansible
ansible-playbook -i localhost, ops/production.yml
```

If sudo requires a password, add `--ask-become-pass`. The playbook targets the local VM, the `minikube` context and the `default` namespace. Run it again to check the deployment after a VM restart. The Deployment manifest controls which image is applied. Update its tag when moving to v2.

### Capture Task 3 evidence

Save the terminal output including the play recap. From the same VM and login, run:

```bash
kubectl --context=minikube -n default get deploy,pods,svc -o wide
kubectl --context=minikube -n default rollout status deployment/weather-ml-app
NODE_IP=$(sg docker -c 'minikube ip -p minikube')
curl --fail "http://${NODE_IP}:30080/"
```

Look for two ready replicas, a NodePort of 30080, and the weather form in the response. This checks availability; the published v1 has a known prediction bug. The readiness probe and rolling update strategy keep existing ready pods available while replacement pods start.

For the browser demonstration, the Minikube node has an internal address. If the lab permits external access, restrict inbound TCP 5000 in the VM's security group to the demonstrator's IP. For the recording, run the following on the VM in a separate terminal and leave it running. The relay targets the Service's NodePort so individual pod replacements do not change its destination.

```bash
sudo apt-get install -y socat
NODE_IP=$(sg docker -c 'minikube ip -p minikube')
socat TCP4-LISTEN:5000,reuseaddr,fork "TCP4:${NODE_IP}:30080"
```

Open `http://<VM-public-IP>:5000/` in the browser. After recording, stop the relay with Ctrl+C and remove the temporary inbound rule.
