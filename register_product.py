import argparse
from tasks.Registrar import Registrar

def parse_args():
    parser = argparse.ArgumentParser(description='Registrar produtos de um arquivo PDF.')
    parser.add_argument('arquivo', help='Caminho do arquivo PDF')
    parser.add_argument('margem', type=float, help='Valor da margem')
    parser.add_argument('cst', help='Valor do CST')
    parser.add_argument('aliquota', help='Valor da alíquota')
    parser.add_argument('tempo_seguranca', type=float, help='Valor do tempo de segurança')
    parser.add_argument('pct', type=int, help='Limiar de similaridade em porcentagem')
    #parser.add_argument('-banco_dados', help='Caminho do arquivo do banco de dados')
    parser.add_argument('-qtd', type=int, help='Quantidade de produtos a serem registrados')
    return parser.parse_args()

def main():
    args = parse_args()
    product_registrar = Registrar(args.arquivo, args.margem, args.cst, args.aliquota, args.tempo_seguranca, args.pct, args.qtd)
    product_registrar.run()

if __name__ == '__main__':
    main()
