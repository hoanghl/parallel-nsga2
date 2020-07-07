# P-NSGA-II
Thuật toán được nhóm chúng tôi đề xuất dựa trên thuật toán NSGA-II - một thuật toán tối ưu đa mục đối tượng rất phổ biến trong gia đình Giải thuật Gene.

# 1. Cài đặt
- Project sử dụng Python3
- Cài đặt các thư viện sau bằng `pip` hoặc `pipenv`:
  + `nsga-2`

### Lưu ý:
- Nếu dùng `pipenv` thì có thể cài đặt trực tiếp bằng lệnh sau:
> pipenv install
- Nếu muốn dùng `pipenv` mà có phiên bản Python3 nhỏ hơn 3.7 thì có thể chỉnh lại version của Python3 trong file `Pipfile`

# 2. Các bài test
Có tổng cộng 8 bài test nằm ở thư mục `measurements`. Mỗi bài test đều có 3 file là `new_2threads.py`, `new_4threads.py` và `old.py` trong đó file `new*.py` dùng P-NSGA-II, còn file kia dùng thuật toán truyền thống.

Cách chạy như sau (giả sử với bài test **TSP17**):
Từ main directory, chạy lệnh
> python -m measurements.tsp17.new_2threads

hoặc

> python -m measurements.tsp17.new_3threads

