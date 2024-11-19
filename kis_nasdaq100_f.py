import requests
import json
import pandas as pd

def get_future_chart_data(
    app_key: str,
    app_secret: str,
    token: str, 
    close_date: str,
    symbol: str,
    exchange: str,
    qry_gap: str = "5",
    is_first: str = "Q",
    index_key: str = ""
):
    """
    해외선물 분봉 조회 API를 호출하는 함수
    
    Args:
        app_key (str): 한국투자증권에서 발급받은 API 키
        app_secret (str): 한국투자증권에서 발급받은 시크릿 키
        start_date (str): 조회 시작일시 (YYYYMMDD)
        close_date (str): 조회 종료일시 (YYYYMMDD)
        symbol (str): 종목코드
        exchange (str): 거래소코드
        qry_gap (str): 분봉 간격
    
    Returns:
        dict: API 응답 데이터
    """
    
    # API 엔드포인트
    base_url = "https://openapi.koreainvestment.com:9443"
    endpoint = "/uapi/overseas-futureoption/v1/quotations/inquire-time-futurechartprice"
    
    # API 요청 헤더
    headers = {
        "content-type": "application/json; charset=utf-8",
        "authorization": token,
        "appkey": app_key,
        "appsecret": app_secret,
        "tr_id": "HHDFC55020400",
        "tr_cont":"",
        "custtype": "P",  # 개인
    }
    
    # Query parameters
    params = {
        "SRS_CD": symbol,
        "EXCH_CD": exchange,
        "START_DATE_TIME": "",
        "CLOSE_DATE_TIME": close_date,
        "QRY_TP": is_first,  # 최초 조회
        "QRY_CNT": "120",  # 최대 조회 건수
        "QRY_GAP": qry_gap,
        "INDEX_KEY": index_key,  # 최초 조회시 공백
    }
    
    try:
        # API 요청
        response = requests.get(
            base_url + endpoint,
            headers=headers,
            params=params
        )
        
        # 응답 확인
        response.raise_for_status()
        
        # JSON 응답 파싱
        data = response.json()
        
        # 응답 코드 확인
        if data["rt_cd"] != "0":
            raise Exception(f"API Error: {data['msg1']}")
            
        return data
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")
    except json.JSONDecodeError as e:
        raise Exception(f"JSON decode error: {str(e)}")
    except Exception as e:
        raise Exception(f"Error occurred: {str(e)}")

# 사용 예시
if __name__ == "__main__":
    # API 키 설정
    APP_KEY = "app_key" # 한국투자증권에서 발급받은 API 키
    APP_SECRET = "app_secret" # 한국투자증권에서 발급받은 시크릿 키
    TOKEN = "Bearer token" # API 토큰


    # 파라미터 설정
    close_date = "20241119"
    symbol = "NQZ24"
    exchange = "CME"
    qry_gap = "10"
    
    args = {
        "app_key":APP_KEY,
        "app_secret":APP_SECRET,
        "token":TOKEN,
        "close_date":close_date,
        "symbol":symbol,
        "exchange":exchange,
        "qry_gap":qry_gap,
        "is_first":"Q",
        "index_key":""
    }
    total_df = pd.DataFrame()
    # while True:
    try:
        result = get_future_chart_data(**args)
        
        print("API Response:")

        df = pd.DataFrame(result['output1'])
        df = df.sort_values(by=["data_date", "data_time"])
        total_df = pd.concat([total_df, df])
        print(df)

        index_key = result['output2']['index_key']
        print(result['output2'])

        if len(index_key) > 10:
            args['is_first'] = "P"
            args['index_key'] = index_key
            # result = get_future_chart_data(**args)
            # df = pd.DataFrame(result['output1'])
            # df = df.sort_values(by=["data_date", "data_time"])
            # print(df)
        # else:
        #     break
            
            
    except Exception as e:
        print(f"Error: {str(e)}")
        
    # if len(total_df) > 0:
    #     path = f'./{symbol}.csv'
    #     total_df = total_df.sort_values(by=["data_date", "data_time"])
    #     total_df.to_csv(path, index=False)