# # Imports

from bs4 import BeautifulSoup
import requests
import pandas as pd
import urllib.parse

import datetime
import os
import cloudscraper
import xlsxwriter
import time

# # HTTP Request

# ## Store website in variable / Get Request with Cloud Scraper

site = 'https://www.autoevolution.com/cars/'
response = cloudscraper.CloudScraper().get(site)  # CloudScraper inherits from requests.Session

# response = requests.get(site)
# response = scraper.get(site)
# scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
# Or: scraper = cloudscraper.CloudScraper()  # CloudScraper inherits from requests.Session


# # Target necessary data


# Brand / BrandLogoUrl / BrandLink
# Model / CarType / ModelYear / ModelImgUrl / ModelLink
# VariantBrand / VariantModel / VariantYear / VariantImgUrl / VariantLink
# BigImageBrand / BigImageTitle / BigImageUrl / BigImageThumb


# # Brand Soup & Results & Status Code


soup = BeautifulSoup(response.content, 'html.parser')
results = soup.find_all('div', {'itemtype': 'https://schema.org/Brand'})
print(response.status_code, " - ", len(results))
# results


# ## Brand / Logo URL / Link


i = 0
rBrand = results[i].find('a').get('title').replace(" models and specs", "")  # brand
rBrandLogoUrl = results[i].find('img').get('src')  # logo url
rBrandLink = results[i].find('a').get('href')  # link

print(rBrand, "\n", rBrandLogoUrl, "\n", rBrandLink)

# # Model Soup & Results


responseModel = cloudscraper.CloudScraper().get(rBrandLink)
soupModel = BeautifulSoup(responseModel.content, 'html.parser')
resultsModel = soupModel.find_all('div', {'class': 'carmod'})
print(responseModel.status_code, " - ", len(resultsModel))
# soupModel


# ## Model / CarType / Year / Image URL / Link


i = 0
rModel = resultsModel[i].find('h4').get_text()  # model
rCarType = resultsModel[i].find('p', {'class': 'body'}).get_text()  # car type
rmYear = resultsModel[i].find('div', {'class': 'col3width fl'}).find('span').get_text()  # year
rmImageUrl = resultsModel[i].find('img').get('src')  # image url
rmLink = resultsModel[i].find('a').get('href')  # link

print(rModel, "\n", rCarType, "\n", rmYear, "\n", rmImageUrl, "\n", rmLink)

# # Variant Soup & Results


responseVariant = cloudscraper.CloudScraper().get(rmLink)
soupVariant = BeautifulSoup(responseVariant.content, 'html.parser')
resultsVariant = soupVariant.find_all('div', {'class': 'container carmodel clearfix'})
print(responseVariant.status_code, " - ", len(resultsVariant))
# resultsVariant


# ## Brand / Model / Year / Image URL / Link


i = 0
rvBrand = resultsVariant[i].find('b', {'itemprop': 'brand'}).get_text()  # brand
rvModel = resultsVariant[i].find('span', {'class': 'col-red'}).get_text()  # model
rvYear = resultsVariant[i].find('p', {'class': 'years'}).find('a').get_text()  # year
rvImageUrl = resultsVariant[i].find('img', {'itemprop': 'image'}).get('src')  # image url
bigImageLink = resultsVariant[i].find('a', {'itemprop': 'url'}).get('href')  # link

print(rvBrand, "\n", rvModel, "\n", rvYear, "\n", rvImageUrl, "\n", bigImageLink)

# # Big Image Soup & Results


responseBigImage = cloudscraper.CloudScraper().get(bigImageLink)
soupBigImage = BeautifulSoup(responseBigImage.content, 'html.parser')
resultsBigImage = soupBigImage.find('div', {'data-itemtype': 'https://schema.org/Car'}).find_all('a',
                                                                                                 {'class': 's_gallery'})
print(responseBigImage.status_code, " - ", len(resultsBigImage))
# resultsBigImage[0]

# ## Brand / Title / Image URL


for i in range(len(resultsBigImage)):
    print(resultsBigImage[i].find('img').get('data-description').replace("Photo credits: ", ""))  # brand
    print(resultsBigImage[i].get('title'))  # title
    print(resultsBigImage[i].get('href'))  # big image
    print(resultsBigImage[i].find('img').get('src'))  # big image thumbnail

# # Put everything together inside a For-Loop

# ## Brand Loop


# Brand / BrandLogoUrl / BrandLink
brandList = []
brandLogoUrlList = []
brandLinkList = []

brandList.clear()
brandLogoUrlList.clear()
brandLinkList.clear()

for i in range(len(results)):

    print(results[i].find('a').get('title').replace(" models and specs", ""))  # brand
    try:
        brandList.append(results[i].find('a').get('title').replace(" models and specs", ""))
    except:
        brandList.append('n/a')

    print(results[i].find('img').get('src'))  # brand logo url
    try:
        brandLogoUrlList.append(results[i].find('img').get('src'))
    except:
        brandLogoUrlList.append('n/a')

    print(results[i].find('a').get('href'))  # brand link
    try:
        brandLinkList.append(results[i].find('a').get('href'))
    except:
        brandLinkList.append('n/a')

# ## Model Loop


# (Brand) / Model / CarType / ModelYear / ModelImgUrl / ModelLink
mBrandList = []
modelList = []
carTypeList = []
mYearList = []
mImgUrlList = []
mLinkList = []

mBrandList.clear()
modelList.clear()
carTypeList.clear()
mYearList.clear()
mImgUrlList.clear()
mLinkList.clear()

for i in range(len(results)):
    for x in range(9):
        print('x değeri: ', x)

        print("Brand: ", brandList[i])
        responseModel = cloudscraper.CloudScraper().get(brandLinkList[i])
        soupModel = BeautifulSoup(responseModel.content, 'html.parser')
        resultsModel = soupModel.find_all('div', {'class': 'carmod'})

        if len(resultsModel) != 0:

            for j in range(len(resultsModel)):

                print(brandList[i])  # brand
                try:
                    mBrandList.append(brandList[i])
                except:
                    mBrandList.append('n/a')

                print(resultsModel[j].find('h4').get_text())  # model
                try:
                    modelList.append(resultsModel[j].find('h4').get_text())
                except:
                    modelList.append('n/a')

                print(resultsModel[j].find('p', {'class': 'body'}).get_text())  # car type
                try:
                    carTypeList.append(resultsModel[j].find('p', {'class': 'body'}).get_text())
                except:
                    carTypeList.append('n/a')

                print(resultsModel[j].find('div', {'class': 'col3width fl'}).find('span').get_text())  # model year
                try:
                    mYearList.append(resultsModel[j].find('div', {'class': 'col3width fl'}).find('span').get_text())
                except:
                    mYearList.append('n/a')

                print(resultsModel[j].find('img').get('src'))  # model image url
                try:
                    mImgUrlList.append(resultsModel[j].find('img').get('src'))
                except:
                    mImgUrlList.append('n/a')

                print(resultsModel[j].find('a').get('href'))  # model link
                try:
                    mLinkList.append(resultsModel[j].find('a').get('href'))
                except:
                    mLinkList.append('n/a')
                print('for döngüsü çalıştı')

            break

        elif len(resultsModel) == 0:
            print('continue, else if çalıştı')
            continue
        else:
            print('break, else bloğu çalıştı')
            break

# ## Variant Loop


# (Brand) / (Model) / (CarType) / (Year) / VariantImgUrl / VariantLink
vBrandList = []
vModelList = []
vCarTypeList = []
vYearList = []
vImgUrlList = []
vLinkList = []

vBrandList.clear()
vModelList.clear()
vCarTypeList.clear()
vYearList.clear()
vImgUrlList.clear()
vLinkList.clear()

for i in range(len(mLinkList)):
    for x in range(9):
        print('x değeri: ', x)

        print("Model: ", modelList[i])
        responseVariant = cloudscraper.CloudScraper().get(mLinkList[i])
        soupVariant = BeautifulSoup(responseVariant.content, 'html.parser')
        resultsVariant = soupVariant.find_all('div', {'class': 'container carmodel clearfix'})

        if len(resultsVariant) != 0:

            for j in range(len(resultsVariant)):

                print(resultsVariant[j].find('b', {'itemprop': 'brand'}).get_text())  # brand
                try:
                    vBrandList.append(resultsVariant[j].find('b', {'itemprop': 'brand'}).get_text())
                except:
                    vBrandList.append('n/a')

                print(resultsVariant[j].find('span', {'class': 'col-red'}).get_text())  # model
                try:
                    vModelList.append(resultsVariant[j].find('span', {'class': 'col-red'}).get_text())
                except:
                    vModelList.append('n/a')

                print(carTypeList[i])  # car type
                try:
                    vCarTypeList.append(carTypeList[i])
                except:
                    vCarTypeList.append('n/a')

                print(resultsVariant[j].find('p', {'class': 'years'}).find('a').get_text())  # year
                try:
                    vYearList.append(resultsVariant[j].find('p', {'class': 'years'}).find('a').get_text())
                except:
                    vYearList.append('n/a')

                print(resultsVariant[j].find('img', {'itemprop': 'image'}).get('src'))  # image url
                try:
                    vImgUrlList.append(resultsVariant[j].find('img', {'itemprop': 'image'}).get('src'))
                except:
                    vImgUrlList.append('n/a')

                print(resultsVariant[j].find('a', {'itemprop': 'url'}).get('href'))  # link
                try:
                    vLinkList.append(resultsVariant[j].find('a', {'itemprop': 'url'}).get('href'))
                except:
                    vLinkList.append('n/a')
                print('for döngüsü çalıştı')

            break

        elif len(resultsVariant) == 0:
            print('continue, else if çalıştı')
            continue
        else:
            print('break, else bloğu çalıştı')
            break

# # Import variant links from excel file


fileData = pd.read_excel(r'variantLink.xlsx', sheet_name='variant')
variantLinks = fileData['Variant Link'].values.tolist()

print(fileData)
# print (variantLinks)

print(len(variantLinks))

# ## Big Images Loop


# BigImageBrand / BigImageTitle / BigImageUrl / BigImageThumb
bigImageBrand = []
bigImageTitle = []
bigImageUrl = []
# bigImageThumb = []

bigImageBrand.clear()
bigImageTitle.clear()
bigImageUrl.clear()
# bigImageThumb.clear()

for i in range(len(variantLinks)):

    for x in range(9):
        print('x değeri: ', x)

        print("Variant Link: ", variantLinks[i])
        responseBigImage = cloudscraper.CloudScraper().get(variantLinks[i])
        soupBigImage = BeautifulSoup(responseBigImage.content, 'html.parser')
        resultsBigImage = soupBigImage.find('div', {'data-itemtype': 'https://schema.org/Car'}).find_all('a', {
            'class': 's_gallery'})
        print(responseBigImage.status_code, " - ", len(resultsBigImage))

        if len(resultsBigImage) != 0:
            for j in range(len(resultsBigImage)):

                print(resultsBigImage[j].find('img').get('data-description').replace("Photo credits: ", ""))  # brand
                try:
                    bigImageBrand.append(
                        resultsBigImage[j].find('img').get('data-description').replace("Photo credits: ", ""))
                except:
                    bigImageBrand.append('n/a')

                print(resultsBigImage[j].get('title'))  # title
                try:
                    bigImageTitle.append(resultsBigImage[j].get('title'))
                except:
                    bigImageTitle.append('n/a')

                print(resultsBigImage[j].get('href'))  # image url
                try:
                    bigImageUrl.append(resultsBigImage[j].get('href'))
                except:
                    bigImageUrl.append('n/a')

                # print(resultsBigImage[j].find('img').get('src')) # image thumbnail
                # try:
                #     bigImageThumb.append(resultsBigImage[j].find('img').get('src'))
                # except:
                #     bigImageThumb.append('n/a')
                print('for döngüsü çalıştı')

            break

        elif len(resultsBigImage) == 0:
            print('continue, else if çalıştı')
            continue
        else:
            print('break, else bloğu çalıştı')
            break

# Length brand arrays
print(len(brandList), len(brandLogoUrlList), len(brandLinkList))

# # Create Pandas Brand Dataframe


# Create brand Pandas dataframes from brands.
brand_overview = pd.DataFrame({'Brand': brandList,
                               'Brand Logo URL': brandLogoUrlList,
                               'Brand Link': brandLinkList})
# brand_overview

# Length model arrays
print(len(mBrandList), len(modelList), len(carTypeList), len(mYearList), len(mImgUrlList), len(mLinkList))

# # Create Pandas Model Dataframe


# Create model Pandas dataframes from models.
model_overview = pd.DataFrame({'Brand': mBrandList,
                               'Model': modelList,
                               'Car Type': carTypeList,
                               'Model Year': mYearList,
                               'Model Image URL': mImgUrlList,
                               'Model Link': mLinkList})
# model_overview

# Length variant arrays
print(len(vBrandList), len(vModelList), len(vCarTypeList), len(vYearList), len(vImgUrlList), len(vLinkList))

# # Create Pandas Variant Dataframe


# Create variant Pandas dataframes from variants.
variant_overview = pd.DataFrame({'Variant Brand': vBrandList,
                                 'Variant Model': vModelList,
                                 'Car Type': vCarTypeList,
                                 'Variant Year': vYearList,
                                 'Variant Image URL': vImgUrlList,
                                 'Variant Link': vLinkList})
# variant_overview

# # Create Pandas Big Image Dataframe


# del bigImageBrand[:28840]
# del bigImageTitle[:28840]
# del bigImageUrl[:28840]
# del bigImageThumb[:28840]


# Create big image Pandas dataframes from big images.
bigImage_overview = pd.DataFrame({'Brand': bigImageBrand,
                                  'Title': bigImageTitle,
                                  'Image URL': bigImageUrl})
# bigImage_overview

# # Naming excel file with timestamp


now = datetime.datetime.now()
name = "bigImage " + str(now) + ".xlsx"
name = name.replace(":", "-")

# # Output in Excel


# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter(name, engine='xlsxwriter')

# ## Output Brands - Models - Variants


# Write each dataframe to a different worksheet.

brand_overview.to_excel(writer, sheet_name='Brands')
model_overview.to_excel(writer, sheet_name='Models')
# variant_overview.to_excel(writer, sheet_name='Variants')
# bigImage_overview.to_excel(writer, sheet_name='BigImage')

writer.save()


# # Download Thumbnails


# brandList[1]
# variantImgUrlList[0]
# len(variantImgUrlList)

# ## define downloader

def down(url, dest_folder):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # create folder if it does not exist

    filename = url.split('/')[-1].replace(" ", "_")  # be careful with file names
    file_path = os.path.join(dest_folder, filename)

    r = requests.get(url, stream=True)
    if r.ok:
        print("saving to", os.path.abspath(file_path))
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
    else:  # HTTP status code 4XX/5XX
        print("Download failed: status code {}\n{}".format(r.status_code, r.text))


for i in range(len(vImgUrlList)):
    url = vImgUrlList[i]
    dest_folder = 'Autoevolution Thumbnails/' + vBrandList[i] + '/' + vModelList[i]
    down(url, dest_folder)

# # Download Big Images


for i in range(len(bigImageUrl)):
    url = bigImageUrl[i]
    dest_folder = 'Autoevolution Big Images/' + bigImageBrand[i] + '/' + bigImageTitle[i]
    down(url, dest_folder)


# # IMPORT IMAGES


# ## Import brand informations from excel file


brandL = []
brandLogoUrlL = []

brandL.clear()
brandLogoUrlL.clear()

brandL = pd.read_excel(r'aEvo_2022.xlsx', sheet_name='Brands')['Brand'].values.tolist()
brandLogoUrlL = pd.read_excel(r'aEvo_2022.xlsx', sheet_name='Brands')['Brand Logo URL'].values.tolist()

print(brandL, brandLogoUrlL)
print(len(brandL), len(brandLogoUrlL))

for i in range(len(brandL)):
    url = brandLogoUrlL[i]
    dest_folder = 'Autoevolution/Brand Logo/'
    down(url, dest_folder)

# ## Import model informations from excel file


mBrandL = []
modelL = []
mImgUrlL = []

mBrandL.clear()
modelL.clear()
mImgUrlL.clear()

mBrandL = pd.read_excel(r'aEvo_2022.xlsx', sheet_name='Models')['Brand'].values.tolist()
modelL = pd.read_excel(r'aEvo_2022.xlsx', sheet_name='Models')['Model'].values.tolist()
mImgUrlL = pd.read_excel(r'aEvo_2022.xlsx', sheet_name='Models')['Model Image URL'].values.tolist()

print(mBrandL, modelL, mImgUrlL)
print(len(mBrandL), len(modelL), len(mImgUrlL))

for i in range(len(mBrandL)):
    url = mImgUrlL[i]
    dest_folder = 'Autoevolution/Model Images/' + mBrandL[i]
    down(url, dest_folder)

# ## Import variant informations from excel file


vBrandL = []
vModelL = []
vImgUrlL = []

vBrandL.clear()
vModelL.clear()
vImgUrlL.clear()

vBrandL = pd.read_excel(r'aEvo_2022.xlsx', sheet_name='Variants')['Variant Brand'].values.tolist()
vModelL = pd.read_excel(r'aEvo_2022.xlsx', sheet_name='Variants')['Variant Model'].values.tolist()
vImgUrlL = pd.read_excel(r'aEvo_2022.xlsx', sheet_name='Variants')['Variant Image URL'].values.tolist()

print(vBrandL, vModelL, vImgUrlL)
print(len(vBrandL), len(vModelL), len(vImgUrlL))

for i in range(len(vBrandL)):
    url = vImgUrlL[i]
    dest_folder = 'Autoevolution/Variant Images/' + vBrandL[i]
    down(url, dest_folder)

# ## Import big image informations from excel file


bBrandL = []
bTitleL = []
bImgUrlL = []

bBrandL.clear()
bTitleL.clear()
bImgUrlL.clear()

bBrandL = pd.read_excel(r'aEvo_2022.xlsx', sheet_name='BigImages')['Brand'].values.tolist()
bTitleL = pd.read_excel(r'aEvo_2022.xlsx', sheet_name='BigImages')['Title'].values.tolist()
bImgUrlL = pd.read_excel(r'aEvo_2022.xlsx', sheet_name='BigImages')['ImageURL'].values.tolist()

print(len(bBrandL), len(bTitleL), len(bImgUrlL))
# print (bBrandL, bTitleL, bImgUrlL)


for i in range(len(bBrandL)):
    url = bImgUrlL[i]
    dest_folder = 'Autoevolution/Big Images/' + bBrandL[i] + '/' + bTitleL[i]
    down(url, dest_folder)

print("Kodun sonu, teşekkürler...")
