podTemplate(label: 'buildah-build',
    yaml: '''
        apiVersion: v1
        kind: Pod
        spec:
          containers:
          - name: git
            image: alpine/git
            command: ["cat"]
            tty: true
          - name: buildah
            image: quay.io/buildah/stable
            command: ["cat"]
            tty: true
            securityContext:
              capabilities:
                add: ["SYS_ADMIN"]
            resources:
              limits:
                smarter-devices/fuse: 1
              requests:
                smarter-devices/fuse: 1
            volumeMounts:
            - mountPath: /var/lib/containers
              name: volume-0
          - name: podman
            image: quay.io/podman/stable
            command: ["cat"]
            tty: true
            volumeMounts:
            - mountPath: /var/lib/containers
              name: volume-0
          - name: argo
            image: 'argoproj/argo-cd-ci-builder:latest'
            command: ["cat"]
            tty: true
         ''',
    volumes: [emptyDirVolume(mountPath: '/var/lib/containers', memory: false)]
) {
    node('buildah-build') {

        stage('Checkout'){
            container('git'){
                checkout scm
            }
        }
        
        stage('Build'){
            container('buildah'){
                script {
                    sh "buildah bud -t 10.43.145.201:5000/python_news_clipper:${env.BUILD_NUMBER} ."
                }
            }
        }

        stage('Push'){
            container('podman'){
                script {
                    sh "podman push 10.43.145.201:5000/python_news_clipper:${env.BUILD_NUMBER} --tls-verify=false"
                }
            }
        }

        stage('Deploy'){
            container('argo'){
                checkout scm

                sshagent(credentials: ['jenkins-ssh-private']){
                    sh("""
                        #!/usr/bin/env bash
                        set +x
                        export GIT_SSH_COMMAND="ssh -oStrictHostKeyChecking=no"
                        git config --global user.email "sepaper@naver.com"
                        git checkout master
                        cd deploy/patch && kustomize edit set image 10.43.145.201:5000/python_news_clipper:${env.BUILD_NUMBER}
                        cd .. && kustomize build patch > deployment.yaml
                        git add deployment.yaml
                        git commit -a -m "update image version into ${env.BUILD_NUMBER}"
                        git push
                    """)
                }
            }
        }
    
    }
    
}