from src.database import SessionLocal, Base, engine
from src.models.funcionario import Funcionario
from src.models.veiculo import Passeio
from src.models.enums import CorVeiculoEnum, TipoVeiculoEnum, StatusVeiculoEnum
from src.seguranca import obter_hash_senha

# 1. FORÇAR A CRIAÇÃO LIMPA
print("🏗️  Criando tabelas de forma controlada...")
Base.metadata.drop_all(bind=engine) # Garante que está limpo
Base.metadata.create_all(bind=engine) # Cria tudo de uma vez

db = SessionLocal()

# 2. CRIAR ADMIN
print("👤 Criando Admin...")
admin = Funcionario(
    email="admin@frotanext.com",
    nome_completo="Admin Root",
    senha=obter_hash_senha("admin123"),
    e_admin=True,
    e_ativado=True
)
db.add(admin)

# 3. CRIAR UM CARRO BÁSICO
print("🚗 Criando Carro de Teste...")
carro = Passeio(
    placa="TEST-0001",
    marca="Fiat",
    modelo="Mobi",
    cor=CorVeiculoEnum.BRANCO,
    valor_diaria=100.00,
    ano_fabricacao=2024,
    ano_modelo=2024,
    chassi="CHASSI0000TESTE",
    capacidade_tanque=45.0,
    cambio_automatico=False,
    ar_condicionado=True,
    status=StatusVeiculoEnum.DISPONIVEL,
    tipo_veiculo=TipoVeiculoEnum.PASSEIO,
    tipo_carroceria="Hatch",
    qtde_portas=4,
    qtde_passageiros=5
)
db.add(carro)

db.commit()
db.close()
print("✅ Banco pronto e sem erros!")
exit()