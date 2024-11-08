FROM prefecthq/prefect:2.6.8-python3.9


COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./scripts/aliases.sh .
RUN cat ./aliases.sh >> ~/.bashrc

COPY ./meltano.yml .

RUN meltano install

COPY . .