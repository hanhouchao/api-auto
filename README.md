# What is this repository for?

1. 该仓库是用来测试标注产品的API测试，使用的python pytest测试框架
2. pytest会自动收集指定目录下所有以<测试>开头的方法作为测试的case，并且最终会在Report下生成测试报告

# RUN E2E
本地执行：

1.首先运行环境需要安装python3+和pytest以及requests包，参考requirement.txt
解决本地python环境问题文档：https://www.jianshu.com/p/00af447f0005

2.最后通过执行pytest <test_path>即可

容器执行：

1.下载镜像 index.alauda.cn/alaudak8s/ares

2.然后需要准备测试对象的环境变量写入一个环境变量文件，具体设置和本地运行一致。然后在运行容器时将这个环境变量文件挂载到容器

3.执行命令：
docker run -t --name vipercd \
	-v $(pwd)/report:/app/report/ \
	--env-file=./local-test.env \
	index.alauda.cn/alaudak8s/ares

