# 🛍️🛒DATA-PIPELINE-LAZADA
Một hệ thống Pipeline xử lý dữ liệu từ sàn thương mại điện tử Lazada: 
Crawl dữ liệu sản phẩm → Lưu trữ vào HDFS (Hadoop Distributed File System) → Xử lý bằng PySpark → Lưu kết quả vào MongoDB để phân tích hoặc hiển thị - trực quan hóa và phân tích
--> Xem chi tiết [báo_cáo]()
## 📂 Mô hình hệ thống 

```
+------------+       +-------------+        +-----------+        +-------------+
|            |       |             |        |           |        |             |
|  Crawler   +-----> |  HDFS (Hadoop)+----> |  PySpark  +------> |   MongoDB   |
| (Selenium) |       |  (Ubuntu VM) |        | (Processing)      | (Storage)   |
+------------+       +-------------+        +-----------+        +-------------+

```

![image](https://github.com/user-attachments/assets/6b386765-0c1a-4bf1-a584-8cee913db1f4)

## 🧰 Công nghệ sử dụng
* Web Crawler: Selenium, Requests, BeautifulSoup
* Big Data: Hadoop (HDFS - với 1 master + 1 slave node)
* Xử lý dữ liệu: PySpark
* Cơ sở dữ liệu: MongoDB Atlas
* DevOps: Ubuntu, Window
* Ngôn ngữ: Python 3.10+
* Đa luồng: Thread

## ⚙️ Cài đặt môi trường Hadoop
### 1. Cài đặt môi trường ubuntu
* 1.1 Tải xuống [ubuntu](https://ubuntu.com/download/desktop/thank-you?version=24.04.1&architecture=amd64&lts=true)
* 1.2 Thiết lập Virualbox ( Network -> Attached to: Bridged Adapter )
* 1.3 Thêm add file ubuntu lên máy ảo virualbox
* 1.4 Cập nhật: `sudo apt update`
  - Cài java phù hợp với hadoop `sudo apt install openjdk-8-jdk -y`
  - Kiểm tra đường dẫn môi trường `which javac ` và `readlink -f path` path là kết quả which javac và đường dẫn java thường là `/usr/lib/jvm/java-8-openjdk-amd64`
### 2. Tải hadoop 
* 2.1 terminal run `wget https://dlcdn.apache.org/hadoop/common/hadoop-3.4.0/hadoop-3.4.0.tar.gz`
* 2.2 Giải nén tệp: tar xzf hadoop-3.4.0.tar.gz
* 2.4 Chuyển file hadoop-3.4.0 đã được giải nén về home trong ubuntu 
![image](https://github.com/user-attachments/assets/caa72312-7a98-4d5c-bd02-c826e70a1220)

- Cài OpenSSH tạo khóa: `sudo apt install openssh-server openssh-client –y`
- Tạo và cài đặt SSH Certificates: `ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa`
- Lưu lại thông tin khóa:  `cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys`
- Cấp quyền: `chmod 0600 ~/.ssh/authorized_keys`
- Kiểm tra ssh: `ssh localhost` nhớ IP
  ![image](https://github.com/user-attachments/assets/251dc379-03bb-47cf-af79-66471fe45637)
  
#### Cấu hình các file Hadoop
Mở terminal mở file `cd hadoop-3.4.0` truy cập hadoop `cd etc/hadoop`
* **Cấu hình: bashrc** ( thêm các biến môi trường ) 
  - `gedit ~/.bashrc`
  - Cấu hình file và thêm vào các biến môi trường trong bashrc
```
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export HADOOP_HOME=/home/admin/hadoop-3.4.0
export HADOOP_INSTALL=$HADOOP_HOME
export HADOOP_MAPRED_HOME=$HADOOP_HOME
export HADOOP_COMMON_HOME=$HADOOP_HOME
export HADOOP_HDFS_HOME=$HADOOP_HOME
export YARN_HOME=$HADOOP_HOME
export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
export PATH=$PATH:$HADOOP_HOME/sbin:$HADOOP_HOME/bin
export HADOOP_OPTS="-Djava.library.path=$HADOOP_HOME/lib/native"
```
Lưu ý: admin là tên user_admin 
![image](https://github.com/user-attachments/assets/7c422198-4e17-4c6f-9b40-9d7234b87c93)

  - Lưu thay đổi bashrc `source ~/.bashrc

* **Cấu hình file hadoop-env.sh** ( môi trường của hadoop )
  - `gedit hadoop-env.sh`
  - Thêm địa chỉ vào dòng 28 dưới #JAVA_HOME
  - `export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64`
    ![image](https://github.com/user-attachments/assets/eb6a1c25-a1a8-4d78-a10a-0c07df60c006)
  - Tạo thư mục trung chuyển ( thư mục tạm )
  - `mkdir -p /home/admin/hadoop-3.3.1/tmp`
    ![image](https://github.com/user-attachments/assets/fcc7df1f-b22b-4992-abdb-d7fe3b17f282)
    
* **Cấu hình file core-site.xml**
  - `gedit core-site.xml`

```
<configuration>
<property>
<name>hadoop.tmp.dir</name>
<value>/home/admin/hadoop-3.4.0/tmp</value>
</property>	
<property>
<name>fs.default.name</name	>
<value>hdfs://localhost:9000</value>
</property>
</configuration>
```
**hadoop.tmp.dir**
- Dùng để lưu trữ file tạm, dữ liệu trung gian, metadata, hoặc một số dữ liệu cần thiết trong quá trình thực thi Hadoop.
- Là nơi lưu các file tạm của các dịch vụ như NameNode, DataNode, SecondaryNameNode, v.v.
- Thư mục này nên tồn tại sẵn và Hadoop phải có quyền ghi vào.
 **fs.defaultFS**
  - Định nghĩa địa chỉ mặc định của hệ thống file mà Hadoop sử dụng
  - Nó cho Hadoop biết nên giao tiếp với hệ thống file nào để đọc/ghi dữ liệu.
  - hdfs://localhost:9000 nghĩa là Hadoop sẽ kết nối tới NameNode đang chạy ở localhost (tức máy cục bộ) trên port 9000.

* **Cấu hình Mapred-site.xml**
- `gedit mapred-site.xml`
```
<configuration>
<property>
  <name>mapreduce.framework.name</name> 
  <value>yarn</value> 
</property>
</configuration>
```
- Cấu hình trên chỉ định framework mà MapReduce sử dụng để thực thi các job
* **Tạo hai folder NameNode và DataNode**
`mkdir -p /home/admin/hadoop-3.3.1/data/namenode`
`mkdir -p /home/admin/hadoop-3.3.1/data/datanode`

* **Cấu hình file hdfs-site.xml**
`gedit hdfs-site.xml `

```
<property>
<name>dfs.replication</name>
<value>1</value>
</property>
<property>
<name>dfs.namenode.name.dir</name>
<value>/home/admin/hadoop-3.3.1/data/namenode</value>
</property>
<property>
<name>dfs.datanode.data.dir</name>
<value>/home/admin/hadoop-3.4.0/data/datanode</value>
</property>
<property>
<name>dfs.namenode.rpc-address</name>
<value>0.0.0.0:9000 </value>
</property>
<property>
<name>dfs.webhdfs.enabled </name>
<value>true </value>
</property>
```
**Giải thích**
  - Replication : số bản sao block có trong rack
  - Namenode.name: xác định đường dẫn cục bộ trên máy chủ NameNode nơi metadata của HDFS (thông tin về cấu trúc file, vị trí của các block) sẽ được lưu trữ.
  - Datanode.data: chỉ ra đường dẫn cục bộ trên các máy DataNode nơi dữ liệu thực tế (các block dữ liệu) sẽ được lưu trữ.
  - Namenode.rpc-address: Xác định địa chỉ và cổng giao tiếp mà NameNode sẽ lắng nghe các yêu cầu từ client và các node khác.
  - Webhdfs.enabled: bật hoặc tắt tính năng WebHDFS, cho phép tương tác với HDFS thông qua các yêu cầu HTTP (REST API).

![image](https://github.com/user-attachments/assets/a3acf5dc-b170-437e-9ead-5108b8ebc825)

* **Cấu hình file Yarn-site.xml**
  - Mở file trong terminal `gedit yarn-site.xml`

```
<property>
  <name>yarn.nodemanager.aux-services</name>
  <value>mapreduce_shuffle</value>
</property>

<property>
  <name>yarn.nodemanager.aux-services.mapreduce.shuffle.class</name>
  <value>org.apache.hadoop.mapred.ShuffleHandler</value>
</property>

<property>
  <name>yarn.resourcemanager.hostname</name>
  <value>127.0.0.1</value>
</property>
<property>
  <name>yarn.acl.enable</name>
  <value>0</value>
</property>
<property>
  <name>yarn.nodemanager.env-whitelist</name>   
<value>JAVA_HOME,HADOOP_COMMON_HOME,HADOOP_HDFS_HOME,HADOOP_CONF_DIR,CLASSPATH_PERPEND_DISTCACHE,HADOOP_YARN_HOME,HADOOP_MAPRED_HOME</value>
</property>
```
**Giải Thích**
 - `yarn.resourcemanager.hostname` Giúp các NodeManager biết địa chỉ của ResourceManager để gửi thông tin tài nguyên, nhận job,...
 - `yarn.acl.enable` Bật/tắt tính năng Access Control List (ACL) — tức là quyền truy cập người dùng
 - `yarn.nodemanager.env-whitelist` Danh sách các biến môi trường (environment variables) được cho phép sử dụng trong NodeManager

* **Chạy hệ thống**
  - Chạy lệnh `hdfs namenode –format`
  - Chạy toàn bộ `start-all.sh`
  - Kiểm tra jps (_có đủ 6 chương trình chạy_) 
  - Có thể truy cập HDFS trên UI `localhost:9870` truy cập Yarn `localhost:8088`
**Đọc thêm chi tiết tại file docx**
