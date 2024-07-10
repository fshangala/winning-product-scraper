import base64
import requests
import os

class CopiwinSDK:
  def __init__(self,client_id:str,client_secret:str):
    self.client_id=client_id
    self.client_secret=client_secret
    self.baseUrl="http://localhost:8000"
    self.access_token=self.getAccessToken()
  
  def getAccessToken(self):
    credential=f"{self.client_id}:{self.client_secret}"
    encodedCredential=base64.b64encode(credential.encode("utf-8"))
    response=requests.post(
      f"{self.baseUrl}/accounts/oauth-token/",
      headers={
        "Content-Type":"application/json",
        "Authorization":f"Basic {encodedCredential.decode('utf-8')}",
      },
      json={
        "grant_type":"client_credentials"
      }
    )
    data = response.json()
    if "access_token" in data:
      return data["access_token"]
    else:
      return None
  
  def getStores(self):
    if self.access_token:
      response=requests.get(
        f"{self.baseUrl}/sales-tracker/",
        headers={
          "Authorization":f"Bearer {self.access_token}"
        }
      )
      if response.status_code == 200:
        return response.json()
      else:
        print(response.reason)
        return None
    else:
      return None
  
  def addStoreData(self,store_id:int,data:dict):
    if self.access_token:
      response=requests.post(
        f"{self.baseUrl}/sales-tracker/track-data/",
        headers={
          "Content-Type":"application/json",
          "Authorization":f"Bearer {self.access_token}"
        },
        json={
          "store":store_id,
          "data":data
        }
      )
      if response.status_code == 201:
        return response.json()
      else:
        print(response.reason)
        return None
    else:
      return None