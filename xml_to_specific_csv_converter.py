import os
import glob
import time

def specific_csv_header(file_name):
    fid = open(file_name, 'w')
    fid.write('tracking_key;barcode;recipient_name;recipient_email;recipient_phone_number;recipient_cpf_cnpj;recipient_inscricao_estadual;address_street;address_number;address_complement;vicinity;city;state;zip_code;nf_key;nf_series;nf_number;nf_volume_number;nf_total_volumes;nf_total_value;package_weight_g;package_length_cm;package_width_cm;package_height_cm;delivery_mode;cnpj_sender;brand_name\n')
    fid.close()

def xml_nfe_fix(file_name):
    fid = open(file_name, 'r')
    fid_fix = fid.read()
    fid.close()
    final_fix = fid_fix.replace('><','>\n<').split('\n')
    return final_fix

def tag_fix_general(string):
    a = string.rsplit('</')
    b = a[0].rsplit('>')
    c = b[1].replace(';','')
    return c

def tag_fix_nfekey(string):
    #<infNFe versao="4.00" Id="NFe35211230893496000130550010002140661778714178">
    a = string.rsplit('Id="NFe')
    b = a[1].rsplit('">')
    return b[0]

def csv_fill(new_package, csv_file):
    fid = open(csv_file, 'a')
    fid.write(new_package)
    fid.close()

def new_package(xml_file,csv_file):
    xml_fix = xml_nfe_fix(xml_file)

    csv_fields = {
        "<infNFe" : [], #tracking_key
        "<CNPJ>" : [], #cnpj_sender
        "<xNome>" : [], #recipient_name
        "<CPF>" : [], #recipient_cpf_cnpj
        "<xLgr>" : [], #address_street
        "<nro>" : [], #address_number
        "<xCpl>" : [], #address_complement
        "<xBairro>" : [], #vicinity
        "<xMun>" : [], #city
        "<UF>" : [], #state
        "<CEP>" : [], #zip_code
        "<serie>" : [], #nf_series
        "<nNF>" : [], #nf_number
        "<vBC>" : [] #nf_total_value
    }

    for chave in csv_fields:
        for i in xml_fix:
            if i.find(chave) >= 0:
                if chave == "<infNFe":
                    fixed_tag = tag_fix_nfekey(i)
                else:
                    fixed_tag = tag_fix_general(i)
                csv_fields[chave].append(fixed_tag)
            elif chave == "<CPF>":
                csv_fields["<CPF>"] = csv_fields["<CNPJ>"]

    recipient_name = csv_fields['<xNome>'][2]
    recipient_email = ''
    recipient_phone_number = ''
    recipient_cpf_cnpj = csv_fields['<CPF>'][0]
    recipient_inscricao_estadual = 'ISENTO'
    address_street = csv_fields['<xLgr>'][1]
    address_number = csv_fields['<nro>'][1]
    address_complement = csv_fields['<xCpl>'][len(csv_fields['<xCpl>'])-1]
    vicinity = csv_fields['<xBairro>'][1]
    city = csv_fields['<xMun>'][1]
    state = csv_fields['<UF>'][1]
    zip_code = csv_fields['<CEP>'][1]
    nf_key = csv_fields['<infNFe'][0]
    nf_series = csv_fields['<serie>'][0]
    nf_number = csv_fields['<nNF>'][0]
    nf_volume_number = '1'
    nf_total_volumes = '1'
    nf_total_value = csv_fields['<vBC>'][len(csv_fields['<vBC>'])-1]
    package_weight_g = ''
    package_length_cm = ''
    package_width_cm = ''
    package_height_cm = ''
    delivery_mode = 'XD'
    cnpj_sender = csv_fields['<CNPJ>'][0]
    brand_name = ''
    tracking_key = nf_key
    barcode = nf_key
    
    var_list = [tracking_key,barcode,recipient_name,recipient_email,recipient_phone_number,recipient_cpf_cnpj,recipient_inscricao_estadual,address_street,address_number,address_complement,vicinity,city,state,zip_code,nf_key,nf_series,nf_number,nf_volume_number,nf_total_volumes,nf_total_value,package_weight_g,package_length_cm,package_width_cm,package_height_cm,delivery_mode,cnpj_sender,brand_name]
    
    csv_new_package = ';'.join(var_list)+'\n'

    csv_fill(csv_new_package, csv_file)

result_path = './csv_folder'
result_file = 'resultado_'+time.strftime("%Y%m%d_%H%M%S")+'.csv'
csv_final_path = os.path.join(result_path,result_file)

specific_csv_header(csv_final_path)

entries = './xml_folder'

for xml in glob.glob(os.path.join(entries, '*.xml')):
    new_package(xml,csv_final_path)
    

print('Feito!')