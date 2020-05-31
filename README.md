# parallel-nsga2
The project aims to parallel NSGA-2 by using special techniques to run that algorithm on many threads.

# 1. Cài đặt
- Project sử dụng Python3
- Cài đặt các thư viện sau bằng `pip` hoặc `pipenv`:
  + `nsga-2`

### Lưu ý:
- Nếu dùng `pipenv` thì có thể cài đặt trực tiếp bằng lệnh sau:
> pipenv install
- Nếu muốn dùng `pipenv` mà có phiên bản Python3 nhỏ hơn 3.7 thì có thể chỉnh lại version của Python3 trong file `Pipfile`

# 2. Các bài test
Có tổng cộng 8 bài test nằm ở thư mục `measurements`. Mỗi bài test đều có 2 là `new.py` và `old.py` trong đó file `new.py` dùng thuật toán song song mới, còn file kia dùng thuật toán truyền thống.

Cách chạy như sau (giả sử với bài test **TSP17**):
Từ main directory, chạy lệnh
> python -m measurements.tsp17.new

hoặc

> python -m measurements.tsp17.old
