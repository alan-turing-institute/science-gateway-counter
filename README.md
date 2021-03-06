# Science Gateway Counter

Counter service for Science Gateway. 

### Local deployment

```shell
pip install -r requirements.txt
./run_test.sh
```

### Azure deployment

```
export APP_NAME=Science-Gateway-Counter
az group create --name $APP_NAME --location westeurope
az appservice plan create --name $APP_NAME --resource-group $APP_NAME --sku S1  # use S1 or higher for access to development slots
az webapp create --name $APP_NAME --resource-group $APP_NAME --plan $APP_NAME
az webapp config set --python-version 3.4 --name $APP_NAME --resource-group $APP_NAME # set python version
az webapp config appsettings set --name $APP_NAME --resource-group $APP_NAME --settings APP_CONFIG_NAME=production
```

```
git remote add azure https://<username>@science-gateway-counter.scm.azurewebsites.net/science-gateway-counter.git
git push azure master

```

