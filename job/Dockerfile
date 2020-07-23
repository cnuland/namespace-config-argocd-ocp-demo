FROM ubi8:latest

USER 0
WORKDIR /script
ADD group-label.py /script
RUN rm /etc/rhsm-host && \
    chmod 775 /script && \
    yum repolist > /dev/null && \
    yum update -y && \
    yum install -y python3 python-pip && \
    curl -o jq -L https://github.com/stedolan/jq/releases/download/jq-1.5/jq-linux64 && \
    chmod +x ./jq && \
    cp jq /usr/bin && \
    curl -o oc.tar.gz https://mirror.openshift.com/pub/openshift-v4/clients/ocp/latest/openshift-client-linux.tar.gz && \
    tar -xvf oc.tar.gz && \
    chmod +x ./oc && \
    cp oc /usr/bin
USER 1001