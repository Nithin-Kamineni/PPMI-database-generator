from keras.models import load_model
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from keras.models import load_model

# Import necessary packages
from sklearn.preprocessing import LabelEncoder

# Data preprocessing for numerical data type
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.impute import SimpleImputer

# One-hot encoding for categorical data type
from sklearn.preprocessing import OneHotEncoder

class MLModel:
    def __init__(self):
        self.best_model_KTRES50  = load_model('static/KTRES50_best_model.h5')
        self.best_model_KTRESmax = load_model('static/KTRESmax_best_model.h5')
        self.best_model_KTRESn  = load_model('static/KTRESn_best_model.h5')
        self.best_model_KTRESrel = load_model('static/KTRESrel_best_model.h5')
        self.Data = pd.read_csv("static/Data.csv").dropna()
        self.df_X = self.Data[["Type","TS","HD","Zeta","Charge","Shape", "TM", "CT", "TSz", "TW"]]
        self.new_row = {"Type": "Inorganic", "TS": "Active", "HD": 68.4, "Zeta": 9.3, "Charge": 0.00, "Shape": "Other", "TM": "Xenograft Heterotopic", "CT": "breast", "TSz": 0.175, "TW": 0.21}

    def GetData(self):
        Data = pd.read_csv(os.path.join("static/Data.csv"))

        df  = pd.DataFrame(Data)
        df_X = df[["Type","TS","HD","Zeta","Charge","Shape", "TM", "CT", "TSz", "TW"]]

        # Seperate the varaibles into 'numerical' and 'categorical' types
        # labeling the numerical data types
        cols_num = ['HD','Zeta',"TSz",'TW']

        # labeling the categorical data types
        cols_label = ['Type','TS','Charge','Shape','TM','CT']

        # Encode labels of multiple columns at once
        df_X [cols_label] = df_X [cols_label].apply(LabelEncoder().fit_transform)

        scaler = StandardScaler()
        mscaler = MinMaxScaler()

        Data_num_tr = pd.DataFrame(mscaler.fit_transform(df_X[cols_num]))
        Data_num_tr.columns = list(df_X[cols_num].columns)

        cat_encoder = OneHotEncoder(sparse=False)
        cols_label_1hot = ['TS','TM',"CT",'Shape']
        data_cat_1hot = pd.DataFrame(cat_encoder.fit_transform(df_X[cols_label_1hot]))
        data_cat_1hot.columns = cat_encoder.get_feature_names_out(cols_label_1hot)

        d=pd.DataFrame(0, index=np.arange(len(data_cat_1hot)), columns=data_cat_1hot.columns)
        d[data_cat_1hot.columns] = data_cat_1hot

        preData=pd.concat([Data_num_tr, d], axis=1)

        X = preData.to_numpy()
        return X,df

    def GetDataParams(self):
        # Remove the row with missing data
        self.Data = self.Data.dropna() # you can use 'subset' (e.g., dropna(subset='HD')) to remove the missing value in specific column
        self.Data = self.Data[1:143]
        df  = pd.DataFrame(self.Data)
        print("==========++++++++++++++++++++++++++++")
        columnNames = list(df.columns)
        columnsMap={"Type":"Particle Type",
        "TS":"Targeting Stratergy",
        "HD":"HD",	"Zeta":"Zeta",
        "Charge":"Charge",
        "Shape":"Shape",
        "TM":"Tumor Model",
        "CT":"CT",
        "TSz":"TSz",
        "TW":"Tumor Weight",
        "Dose":"Dose",
        "BW":"Body Weight"}
        colNumerals={"HD","Zeta","TSz","TW","Dose","BW"}
        params={}
        for i in range(1,len(columnNames)-7):
            if(columnNames[i] in colNumerals):
                params[columnsMap[columnNames[i]]]=[min(df[columnNames[i]].unique().tolist()),max(df[columnNames[i]].unique().tolist())]
            else:
                params[columnsMap[columnNames[i]]]=df[columnNames[i]].unique().tolist()
        return params

    def prediction(self,user_input=None):
        if user_input==None:
            user_input={"HD":534, "TS": None}
            
        test_input=self.new_row.copy()
        for key in test_input:
            print(key)
            if(user_input[key]!=None):
                test_input[key]=user_input[key]

        new_row_df = pd.DataFrame(test_input, index=[0])  # Create a DataFrame from the new row
        df_X = pd.concat([new_row_df, self.df_X], ignore_index=True)
        
        

        # labeling the numerical data types
        cols_num = ['HD','Zeta',"TSz",'TW']

        # labeling the categorical data types
        cols_label = ['Type','TS','Charge','Shape','TM','CT']

        print(df_X[0:2])

        # Encode labels of multiple columns at once
        df_X[cols_label] = df_X[cols_label].apply(LabelEncoder().fit_transform)

        scaler = StandardScaler()
        mscaler = MinMaxScaler()

        Data_num_tr = pd.DataFrame(mscaler.fit_transform(df_X[cols_num]))
        Data_num_tr.columns = list(df_X[cols_num].columns)

        cat_encoder = OneHotEncoder(sparse=False)
        cols_label_1hot = ['TS','TM',"CT",'Shape']
        data_cat_1hot = pd.DataFrame(cat_encoder.fit_transform(df_X[cols_label_1hot]))
        data_cat_1hot.columns = cat_encoder.get_feature_names_out(cols_label_1hot)

        d=pd.DataFrame(0, index=np.arange(len(data_cat_1hot)), columns=data_cat_1hot.columns)
        d[data_cat_1hot.columns] = data_cat_1hot

        preData=pd.concat([Data_num_tr, d], axis=1)

        exaData = preData.iloc[0:1,:]

        X = exaData.to_numpy()

        preds_KTRES50   = self.best_model_KTRES50.predict(X)
        preds_KTRESmax  = self.best_model_KTRESmax.predict(X)
        preds_KTRESn   = self.best_model_KTRESn.predict(X)
        preds_KTRESrel  = self.best_model_KTRESrel.predict(X)
        
        Pred_pars = pd.DataFrame({'KTRES50': np.concatenate(preds_KTRES50),
              'KTRESmax': np.concatenate(preds_KTRESmax),
              'KTRESn': np.concatenate(preds_KTRESn),
              'KTRESrel': np.concatenate(preds_KTRESrel)}
              )

        return Pred_pars

    def FilteredRecords(self, data):
        Data = pd.read_csv(os.path.join("static/Data.csv"))
        df  = pd.DataFrame(Data)

        revColumnsMap={"Particle Type":"Type",
        "Targeting Stratergy":"TS",
        "HD":"HD",	"Zeta":"Zeta",
        "Charge":"Charge",
        "Shape":"Shape",
        "Tumor Model":"TM",
        "CT":"CT",
        "TSz":"TSz",
        "Tumor Weight":"TW",
        "Dose":"Dose",
        "Body Weight":"BW"}
        bodykeys=list(data.keys())
        print(df)
        flag=True
        data["IncludeNA-hd"]=flag
        data["IncludeNA-zeta"]=flag
        data["IncludeNA-tsz"]=flag
        data["IncludeNA-tw"]=flag
        data["IncludeNA-dose"]=flag
        data["IncludeNA-bw"]=flag
        print("========================")
        response_df = df[df["Type"].isin(data["Particle Type"]) &
         df["TS"].isin(data["Targeting Stratergy"]) &
         (((df["HD"]>=data["HD"][0]) & (df["HD"]<=data["HD"][1])) | (df["HD"].isnull() & data["IncludeNA-hd"])) &
         (((df["Zeta"]>=data["Zeta"][0]) & (df["Zeta"]<=data["Zeta"][1])) | (df["Zeta"].isnull() & data["IncludeNA-zeta"])) &
         df["Charge"].isin(data["Charge"]) &
         df["Shape"].isin(data["Shape"]) &
         df["TM"].isin(data["Tumor Model"]) &
         df["CT"].isin(data["CT"]) &
         (((df["TSz"]>=data["TSz"][0]) & (df["TSz"]<=data["TSz"][1])) | (df["TSz"].isnull() & data["IncludeNA-tsz"])) &
         (((df["TW"]>=data["Tumor Weight"][0]) & (df["TW"]<=data["Tumor Weight"][1])) | (df["TW"].isnull() & data["IncludeNA-tw"])) &
         (((df["Dose"]>=data["Dose"][0]) & (df["Dose"]<=data["Dose"][1])) | (df["Dose"].isnull() & data["IncludeNA-dose"])) &
         (((df["BW"]>=data["Body Weight"][0]) & (df["BW"]<=data["Body Weight"][1])) | (df["BW"].isnull() & data["IncludeNA-bw"]))]
        
        return df

    def NumberOfRecords(self, data):
        Data = pd.read_csv(os.path.join("static/Data.csv"))
        df  = pd.DataFrame(Data)

        revColumnsMap={"Particle Type":"Type",
        "Targeting Stratergy":"TS",
        "HD":"HD",	"Zeta":"Zeta",
        "Charge":"Charge",
        "Shape":"Shape",
        "Tumor Model":"TM",
        "CT":"CT",
        "TSz":"TSz",
        "Tumor Weight":"TW",
        "Dose":"Dose",
        "Body Weight":"BW"}
        bodykeys=list(data.keys())
        print(df)
        flag=True
        data["IncludeNA-hd"]=flag
        data["IncludeNA-zeta"]=flag
        data["IncludeNA-tsz"]=flag
        data["IncludeNA-tw"]=flag
        data["IncludeNA-dose"]=flag
        data["IncludeNA-bw"]=flag
        print("========================")
        NumberOfRecords = df[df["Type"].isin(data["Particle Type"]) &
         df["TS"].isin(data["Targeting Stratergy"]) &
         (((df["HD"]>=data["HD"][0]) & (df["HD"]<=data["HD"][1])) | (df["HD"].isnull() & data["IncludeNA-hd"])) &
         (((df["Zeta"]>=data["Zeta"][0]) & (df["Zeta"]<=data["Zeta"][1])) | (df["Zeta"].isnull() & data["IncludeNA-zeta"])) &
         df["Charge"].isin(data["Charge"]) &
         df["Shape"].isin(data["Shape"]) &
         df["TM"].isin(data["Tumor Model"]) &
         df["CT"].isin(data["CT"]) &
         (((df["TSz"]>=data["TSz"][0]) & (df["TSz"]<=data["TSz"][1])) | (df["TSz"].isnull() & data["IncludeNA-tsz"])) &
         (((df["TW"]>=data["Tumor Weight"][0]) & (df["TW"]<=data["Tumor Weight"][1])) | (df["TW"].isnull() & data["IncludeNA-tw"])) &
         (((df["Dose"]>=data["Dose"][0]) & (df["Dose"]<=data["Dose"][1])) | (df["Dose"].isnull() & data["IncludeNA-dose"])) &
         (((df["BW"]>=data["Body Weight"][0]) & (df["BW"]<=data["Body Weight"][1])) | (df["BW"].isnull() & data["IncludeNA-bw"]))].shape[0]
        print("=======================")
        return {"NumberOfRecords":NumberOfRecords}

mLModel = MLModel()