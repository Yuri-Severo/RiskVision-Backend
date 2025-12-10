# 🧪 Guia de Testes do RiskVision Dashboard

## Checklist de Testes Manual

### ✅ Pré-requisitos
- [ ] API RiskVision está rodando
- [ ] Dashboard foi iniciado com sucesso
- [ ] Possui credenciais válidas
- [ ] Navegador moderno (Chrome, Firefox, Edge)

---

## 1️⃣ Teste de Autenticação

### Cenário 1: Login com credenciais válidas
1. Acesse http://localhost:8501
2. Digite usuário válido
3. Digite senha válida
4. Clique em "Entrar"
5. **Resultado esperado:** Redirecionamento para dashboard

### Cenário 2: Login com credenciais inválidas
1. Digite usuário incorreto
2. Digite senha incorreta
3. Clique em "Entrar"
4. **Resultado esperado:** Mensagem de erro

### Cenário 3: Campos vazios
1. Deixe campos em branco
2. Clique em "Entrar"
3. **Resultado esperado:** Mensagem "Preencha todos os campos"

### Cenário 4: Logout
1. Após login, vá para sidebar
2. Clique em "🚪 Sair"
3. **Resultado esperado:** Volta para tela de login

---

## 2️⃣ Teste da Página Principal (Overview)

### Cenário 1: Visualização inicial
1. Após login, verifique:
   - [ ] Status do modelo aparece (verde/vermelho)
   - [ ] Cards de métricas carregam
   - [ ] Formulário de previsão está visível
   - [ ] Sidebar mostra username

### Cenário 2: Gerar previsão padrão (60 minutos)
1. Slider em 60 minutos
2. Clique "🚀 Gerar Previsão"
3. Aguarde spinner
4. **Resultado esperado:**
   - [ ] Mensagem de sucesso
   - [ ] Gráfico aparece com histórico + previsões
   - [ ] Área azul de confiança visível
   - [ ] 4 cards de métricas atualizam
   - [ ] Tabela mostra previsões

### Cenário 3: Gerar previsão com horizonte mínimo (1 min)
1. Ajuste slider para 1
2. Clique "Gerar Previsão"
3. **Resultado esperado:** Previsão com 1 ponto

### Cenário 4: Gerar previsão com horizonte máximo (100 min)
1. Ajuste slider para 100
2. Clique "Gerar Previsão"
3. **Resultado esperado:** Previsão com ~100 pontos

### Cenário 5: Download CSV
1. Após gerar previsão
2. Clique "📥 Download CSV"
3. **Resultado esperado:** Arquivo baixado com dados

### Cenário 6: Expandir informações do modelo
1. Clique em "ℹ️ Informações do Modelo"
2. **Resultado esperado:** Mostra versão, data, amostras

### Cenário 7: Auto-refresh
1. Na sidebar, selecione "30 segundos"
2. Aguarde 30 segundos
3. **Resultado esperado:** Página recarrega automaticamente

---

## 3️⃣ Teste da Página de Análise Histórica

### Cenário 1: Navegação
1. Na sidebar, clique "📈 Historical"
2. **Resultado esperado:** Carrega página de análise

### Cenário 2: Carregar dados padrão
1. Verifique filtros padrão (100 registros, Candlestick)
2. **Resultado esperado:**
   - [ ] 5 cards de estatísticas aparecem
   - [ ] Gráfico candlestick + volume carrega
   - [ ] Valores parecem corretos

### Cenário 3: Alterar período
1. Selecione "Últimos 200 registros"
2. **Resultado esperado:** Gráfico atualiza com mais dados

### Cenário 4: Trocar tipo de gráfico
1. Selecione "Linha"
2. **Resultado esperado:** Gráfico muda para linha com MA

### Cenário 5: Trocar tipo para Área
1. Selecione "Área"
2. **Resultado esperado:** Gráfico com preenchimento

### Cenário 6: Ajustar média móvel
1. Selecione "50 períodos"
2. **Resultado esperado:** Linha amarela mais suave

### Cenário 7: Atualizar dados
1. Clique "🔄 Atualizar Dados"
2. **Resultado esperado:** Cache limpo e dados recarregam

### Cenário 8: Aba "Dados Tabulares"
1. Clique na aba "📋 Dados"
2. **Resultado esperado:**
   - [ ] Tabela com últimos 20 registros
   - [ ] Colunas formatadas
   - [ ] Botão de download aparece

### Cenário 9: Download histórico
1. Na aba Dados, clique "📥 Download CSV Completo"
2. **Resultado esperado:** Arquivo CSV baixado

### Cenário 10: Aba "Distribuição"
1. Clique na aba "📊 Distribuição"
2. **Resultado esperado:**
   - [ ] Histograma de preços
   - [ ] Box plot

### Cenário 11: Aba "Retornos"
1. Clique na aba "📈 Retornos"
2. **Resultado esperado:**
   - [ ] Gráfico de retornos diários
   - [ ] 4 métricas (média, desvio, máx, mín)

---

## 4️⃣ Teste da Página de Configurações

### Cenário 1: Navegação
1. Na sidebar, clique "⚙️ Settings"
2. **Resultado esperado:** Carrega página de configurações

### Cenário 2: Verificar status da conexão
1. Observe seção "🌐 Status da Conexão"
2. **Resultado esperado:**
   - [ ] Mostra "Online ✅" se API rodando
   - [ ] Mostra URL correta

### Cenário 3: Informações do modelo
1. Verifique 4 cards de info
2. **Resultado esperado:**
   - [ ] Status (HEALTHY)
   - [ ] Modelo treinado (Sim/Não)
   - [ ] Data da última previsão
   - [ ] Total de previsões

### Cenário 4: Retreinar modelo
1. Clique "🚀 Retreinar Agora"
2. Aguarde spinner
3. **Resultado esperado:**
   - [ ] Mensagem de sucesso
   - [ ] Balloons animam 🎈

### Cenário 5: Limpar cache
1. Clique "🧹 Limpar Cache"
2. **Resultado esperado:** Mensagem "Cache limpo"

### Cenário 6: Atualizar dados
1. Clique "♻️ Atualizar"
2. **Resultado esperado:** Página recarrega

### Cenário 7: Informações da sessão
1. Verifique 3 cards de sessão
2. **Resultado esperado:**
   - [ ] Nome de usuário correto
   - [ ] Data/hora de login
   - [ ] Duração da sessão

### Cenário 8: Logs recentes
1. Role até "📋 Logs Recentes"
2. **Resultado esperado:**
   - [ ] Mostra últimas entradas
   - [ ] Cores por nível (INFO, WARNING, ERROR)
   - [ ] Timestamps corretos

### Cenário 9: Configurações avançadas
1. Expanda "⚙️ Configurações do Dashboard"
2. Altere algumas opções
3. Clique "💾 Salvar Configurações"
4. **Resultado esperado:** Mensagem de sucesso

### Cenário 10: Debug mode
1. Expanda "🐛 Debug Mode"
2. **Resultado esperado:**
   - [ ] JSON do session_state
   - [ ] JSON do health check

---

## 5️⃣ Testes de Responsividade

### Desktop (1920x1080)
1. Abra em resolução desktop
2. **Verificar:**
   - [ ] Sidebar visível por padrão
   - [ ] Gráficos em tamanho cheio
   - [ ] Métricas em 4-5 colunas

### Tablet (768x1024)
1. Redimensione para ~768px
2. **Verificar:**
   - [ ] Layout ajusta
   - [ ] Gráficos redimensionam
   - [ ] Métricas em 2-3 colunas

### Mobile (375x667)
1. Redimensione para ~375px (ou use DevTools)
2. **Verificar:**
   - [ ] Sidebar vira hambúrguer
   - [ ] Gráficos em largura total
   - [ ] Métricas empilhadas (1 coluna)
   - [ ] Botões em tamanho total

---

## 6️⃣ Testes de Erro

### Cenário 1: API offline
1. Pare a API: `docker stop riskvision-api`
2. Tente gerar previsão
3. **Resultado esperado:** Erro de conexão
4. Reinicie API: `docker start riskvision-api`

### Cenário 2: Token expirado
1. Aguarde tempo de expiração do token (se configurado)
2. Tente fazer ação
3. **Resultado esperado:** Redireciona para login

### Cenário 3: Dados vazios
1. Se API retornar dados vazios
2. **Resultado esperado:** Mensagem "Nenhum dado disponível"

### Cenário 4: Timeout
1. Configure API_TIMEOUT=1 no .env
2. Tente carregar dados grandes
3. **Resultado esperado:** Erro de timeout

---

## 7️⃣ Testes de Performance

### Cenário 1: Carga inicial
1. Limpe cache do navegador
2. Acesse dashboard
3. **Verificar:** Carrega em < 3 segundos

### Cenário 2: Gráfico com muitos dados
1. Carregue 1000 registros históricos
2. **Verificar:** Gráfico renderiza em < 2 segundos

### Cenário 3: Auto-refresh não trava
1. Configure auto-refresh 30s
2. Aguarde 5 minutos
3. **Verificar:** Dashboard continua responsivo

### Cenário 4: Múltiplas abas
1. Abra dashboard em 3 abas
2. **Verificar:** Todas funcionam independentemente

---

## 8️⃣ Testes de Navegação

### Cenário 1: Navegação entre páginas
1. Overview → Historical → Settings → Overview
2. **Verificar:** Todas carregam sem erro

### Cenário 2: Refresh manual
1. Pressione F5 em qualquer página
2. **Verificar:** Página recarrega corretamente

### Cenário 3: Voltar/Avançar do navegador
1. Use botões ← → do navegador
2. **Verificar:** Navegação funciona

### Cenário 4: Link direto
1. Acesse http://localhost:8501/?page=Historical
2. **Verificar:** Vai direto para página (se autenticado)

---

## 9️⃣ Testes de Interatividade

### Cenário 1: Hover em gráficos
1. Passe mouse sobre pontos do gráfico
2. **Verificar:** Tooltip aparece com valores

### Cenário 2: Zoom em gráficos
1. Use scroll ou selecione área
2. **Verificar:** Gráfico dá zoom

### Cenário 3: Pan em gráficos
1. Arraste gráfico
2. **Verificar:** Move visualização

### Cenário 4: Legendas clicáveis
1. Clique em itens da legenda
2. **Verificar:** Mostra/oculta série

### Cenário 5: Reset do gráfico
1. Após zoom, clique em "Reset axes"
2. **Verificar:** Volta ao zoom original

---

## 🔟 Testes de Segurança

### Cenário 1: Acesso sem login
1. Limpe session_state
2. Tente acessar página protegida
3. **Resultado esperado:** Redireciona para login

### Cenário 2: XSS básico
1. Tente inserir `<script>alert('xss')</script>` em inputs
2. **Resultado esperado:** Escapado/sanitizado

### Cenário 3: SQL Injection (não aplicável, mas verificar)
1. Inputs são validados antes de enviar para API
2. **Verificar:** Sem inputs diretos para banco

---

## 📊 Relatório de Testes

### Após completar, preencha:

**Data:** ___/___/______

**Testador:** _______________

**Ambiente:**
- [ ] Local
- [ ] Docker
- [ ] Docker Compose

**Navegador:**
- [ ] Chrome
- [ ] Firefox
- [ ] Edge
- [ ] Safari

**Resultados:**
- Total de cenários testados: ___
- Cenários passaram: ___
- Cenários falharam: ___
- Bugs encontrados: ___

**Bugs/Issues:**
1. ________________________________
2. ________________________________
3. ________________________________

**Observações:**
________________________________
________________________________
________________________________

---

## 🐛 Reportando Bugs

Se encontrar bugs, inclua:

1. **Título:** Descrição curta do problema
2. **Passos para reproduzir:**
   - Passo 1
   - Passo 2
   - Passo 3
3. **Resultado esperado:** O que deveria acontecer
4. **Resultado obtido:** O que aconteceu
5. **Screenshots:** Se possível
6. **Logs:** Erros do console (F12)
7. **Ambiente:**
   - SO: Windows/Linux/Mac
   - Navegador: Chrome/Firefox/etc
   - Versão: X.Y.Z

---

## ✅ Critérios de Aceitação

O dashboard está pronto para produção se:

- [ ] Todas as 3 páginas carregam sem erro
- [ ] Autenticação funciona corretamente
- [ ] Gráficos renderizam dados reais
- [ ] Não há erros no console do navegador
- [ ] Responsivo em desktop e mobile
- [ ] Performance aceitável (< 3s carga inicial)
- [ ] Error handling funciona (exibe mensagens)
- [ ] Auto-refresh funciona sem travar
- [ ] Download de dados funciona
- [ ] Logout funciona corretamente

---

**Boa sorte com os testes! 🧪✅**
