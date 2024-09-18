import csv
import os

from fastapi import HTTPException, status, UploadFile, File


class FileProcessor:
	""" Manager of files and folders processor. """

	def __init__(self):
		self.file_path = 'data/seu_file.csv'
		self.directory = 'data'

	def create_file(self):
		if os.path.exists(self.file_path):
			raise HTTPException(
				status_code=status.HTTP_406_NOT_ACCEPTABLE,
				detail="Arquivo já existe"
			)

		os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
		with open(self.file_path, 'w', newline='') as file:
			writer = csv.writer(file)
			writer.writerow(['conta', 'agencia', 'texto', 'valor'])
		return {"mensagem": f"Arquivo {self.file_path} criado com sucesso"}

	async def upload_file(self, file: UploadFile = File(...)):
		"""
		Upload of file
		:param file:
		:return: Success or Error
		"""
		if not file.filename.endswith('csv'):
			raise HTTPException(
				status_code=status.HTTP_406_NOT_ACCEPTABLE,
				detail="Arquivo no formato não suportado"
			)

		try:
			contents = await file.read()
			decoded_file = contents.decode('utf-8').splitlines()

			csv_reader = csv.DictReader(decoded_file)
			for row in csv_reader:
				print(row)

			return {"mensagem": f"Arquivo {file.filename} criado com sucesso"}
		except Exception as e:
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST,
				detail=f"Falha ao processar o arquivo csv: {str(e)}"
			)

	async def add_data_to_gile(self, data: dict):
		"""
		Add data to file created
		:param data: account data history
		:return:
		"""

		if not os.path.exists(self.file_path):
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="Arquivo inexistente, por favor, acessar a rota para criar o arquivo."
			)

		with open(self.file_path, mode="a", newline='') as file:
			writer = csv.writer(file)
			writer.writerow([data['conta'], data['agencia'], data['texto'], data['valor']])
			return {"mensagem": f"Dados inseridos com sucesso: {data}"}

	async def list_file_data(self, file_name):
		"""
		list data from a file
		:param file_name: file name to list data
		:return:
		"""

		file_path = f"data/{file_name}"
		if not os.path.exists(file_path):
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="Arquivo inexistente, por favor, acessar a rota para criar o arquivo."
			)

		file_data = []
		with open(file_path, mode="r") as file:
			reader = csv.DictReader(file)
			for row in reader:
				file_data.append(row)
		return {f"Dados do arquivo: {file_name}:": file_data}
