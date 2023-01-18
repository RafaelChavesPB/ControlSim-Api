Control-Sim é uma Api que realiza simulação para sistemas de controle visto na disciplina Controle I, para realizar as simulações basta enviar uma requisição POST indicando o tipo de simulação requerida e os resultados serão enviados na resposta do servidor.

## Fields:

A simulação requerida deve ser especificáda através de um pacote Json contendo os seguintes campos:

### *system:
- *num: 
- *num-type:
- *den:
- *den-type:
- gain:
### comp:
- *num: 
- *num-type:
- *den:
- *den-type:
- gain:
### pid:
- kp:
- ki:
- kd:
### feedback:

### plots:

### values:



* indica que o campo é obrigatório.

## Examples:

	{
		"system":{
			"num":"1",
			"num_type":"poly",
			"den":"1 2",
			"den_type":"poly",
			"gain":1
		},
		"comp":{
			"num":"1",
			"num_type":"roots",
			"den":"1 2",
			"den_type":"poly",
			"gain":2
		},
		"plots":["step"],
		"values":["system","poles","zeros"]
	}

