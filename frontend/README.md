# DevSync — frontend

Consulte o [README principal](../README.md) para instalar e executar o frontend junto ao backend Django.

## Instalação
```
npm install
```

### Prévia local
```
npm run serve
```

### Build e sincronização com o Django
```
npm run build
```

### Verificação de código
```
npm run lint -- --no-fix
```

O build grava os arquivos em `../backend/static/frontend/` e atualiza automaticamente o template Django. Para acessar login e dados, use `http://127.0.0.1:8000/devsync/` após iniciar o backend.
