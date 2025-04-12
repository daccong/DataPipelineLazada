# 🛍️🛒DATA-PIPELINE-LAZADA
Một hệ thống Pipeline xử lý dữ liệu từ sàn thương mại điện tử Lazada: 
Crawl dữ liệu sản phẩm → Lưu trữ vào HDFS (Hadoop Distributed File System) → Xử lý bằng PySpark → Lưu kết quả vào MongoDB để phân tích hoặc hiển thị - trực quan hóa và phân tích
## 📂 Mô hình hệ thống 

```
+------------+       +-------------+        +-----------+        +-------------+
|            |       |             |        |           |        |             |
|  Crawler   +-----> |  HDFS (Hadoop)+----> |  PySpark  +------> |   MongoDB   |
| (Selenium) |       |  (Ubuntu VM) |        | (Processing)      | (Storage)   |
+------------+       +-------------+        +-----------+        +-------------+

```
## 🧰 Công nghệ sử dụng
* Web Crawler: Selenium, Requests, BeautifulSoup
* Big Data: Hadoop (HDFS - với 1 master + 1 slave node)
* Xử lý dữ liệu: PySpark
* Cơ sở dữ liệu: MongoDB Atlas
* DevOps: Ubuntu, Window
* Ngôn ngữ: Python 3.10+

# 📦 Cấu trúc thư mục

