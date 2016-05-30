from address_segmentation.segment_api import segment_api_v1_0, segment_api_v1_1

# # http://localhost:8888/?addText=81+Duong+16%2C+P.+Binh+Tri+Dong+B%2C+Q.Binh+Tan%2C+0909218877%2C+Dinh+Thi+Bich+Phuong
# print(segment_api_v1_0('81 Duong 16, P. Binh Tri Dong B, Q.Binh Tan, 0909218877, Dinh Thi Bich Phuong'))
#
# # http://localhost:8888/?addText=Nguyen%20Thi%20Thanh%20Thuy%2C%2036%2F6B%20Quang%20Trung%2C%20P.10%2C%20Q.%20Go%20Vap%2C%200958064086
# print(segment_api_v1_0('Nguyen Thi Thanh Thuy, 36/6B Quang Trung, P.10, Q. Go Vap, 0958064086'))
#
# # http://localhost:8888/?addText=D002%20Lo%20D%20Chung%20Cu%20KCN%20P.Tay%20Thanh%2C%20Pham%20Thi%20Phuong%2C%200903030818
# print(segment_api_v1_0('D002 Lo D Chung Cu KCN P.Tay Thanh, Pham Thi Phuong, 0903030818'))
#
# # http://localhost:8888/?addText=0908%20293%20595%2C%20Lau%202%20TTTM%20Parkson%2C%20126%20Hung%20Vuong%2C%20Q.%205%2C%20Huynh%20Kim%20Danh
# print(segment_api_v1_0('0908 293 595, Lau 2 TTTM Parkson, 126 Hung Vuong, Q. 5, Huynh Kim Danh'))
#
# # http://localhost:8888/?addText=Vu%20Thi%20Bich%20Thuy%2C%20593%2F9%20Nguyen%20Kiem%2C%20P.3%2C%20Q.GV%2C%200909634660
# print(segment_api_v1_0('Vu Thi Bich Thuy, 593/9 Nguyen Kiem, P.3, Q.GV, 0909634660'))
#
# # http://localhost:8888/?addText=098591331%2C%20666%20Tinh%20Lo%2010%2C%20P.%20BTD%2C%20Q.%20B%20Tan%2C%20Huynh%20Van%20Hai
# print(segment_api_v1_0('098591331, 666 Tinh Lo 10, P. BTD, Q. B Tan, Huynh Van Hai'))
#
# # http://localhost:8888/?addText=263%2F11%20Nguyen%20Trai%2C%20Q.1%2C%20Nguyen%20Cong%20Vien%2C%200918030924
# print(segment_api_v1_0('263/11 Nguyen Trai, Q.1, Nguyen Cong Vien, 0918030924'))
#
# # http://localhost:8888/?addText=0989052625%2C%20B%C3%B9i%20H%E1%BB%93ng%20Th%E1%BB%A5y%2C%20B24%20Bis%20C%C6%B0%20X%C3%A1%20Lam%20S%C6%A1n%2C%20Nguy%E1%BB%85n%20Oanh

# print(segment_api_v1_1('263/11 Nguyen Trai, Q.1, Nguyen Cong Vien, 0918030924, abc@gmail.com www.bagasus.com'))

