"""
Template do Agente - Mundo do Wumpus
------------------------------------
INSTRUÇÕES PARA OS ALUNOS:
1. Este script se comunicará automaticamente com o Judge (Avaliador).
2. Não utilize funções como `input()` esperando digitar no teclado. O Judge
   enviará as informações do ambiente diretamente pela entrada padrão do sistema.
3. Sempre que imprimir uma ação usando `print()`, mantenha o parâmetro `flush=True`.
4. As ações permitidas que você deve retornar (exatamente como escrito) são:
   - MOVER
   - VIRAR (E)
   - VIRAR (D)
   - ATIRAR
   - AGARRAR
   - ESCALAR
5. Os sensores que você receberá em uma string separada por vírgulas são:
   CHEIRO, BRISA, BRILHO, CHOQUE, GRITO, OURO, NO ESCADA, ou NADA
"""

import sys
from collections import deque

MOVER = "MOVER"
VIRAR_E = "VIRAR (E)"
VIRAR_D = "VIRAR (D)"
ATIRAR = "ATIRAR"
AGARRAR = "AGARRAR"
ESCALAR = "ESCALAR"
ACOES_VALIDAS = {MOVER, VIRAR_E, VIRAR_D, ATIRAR, AGARRAR, ESCALAR}

# =====================================================================
# ÁREA DO AGENTE IMPLEMENTADO
# =====================================================================

DX = [1, 0, -1, 0]
DY = [0, 1, 0, -1]


def celulas_adjacentes(x, y):
    vizinhos = []
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        nx, ny = x + dx, y + dy
        if 1 <= nx <= 4 and 1 <= ny <= 4:
            vizinhos.append((nx, ny))
    return vizinhos


def bfs_caminho(inicio, destino, celulas_seguras, direcao_inicial):
    if inicio == destino:
        return []
    estado_inicial = (inicio[0], inicio[1], direcao_inicial)
    fila = deque()
    fila.append((estado_inicial, []))
    visitados = {estado_inicial}
    while fila:
        (x, y, direcao), acoes = fila.popleft()
        nx, ny = x + DX[direcao], y + DY[direcao]
        if (nx, ny) in celulas_seguras and 1 <= nx <= 4 and 1 <= ny <= 4:
            novo_estado = (nx, ny, direcao)
            novas_acoes = acoes + [MOVER]
            if (nx, ny) == destino:
                return novas_acoes
            if novo_estado not in visitados:
                visitados.add(novo_estado)
                fila.append((novo_estado, novas_acoes))
        nova_dir_e = (direcao + 1) % 4
        estado_e = (x, y, nova_dir_e)
        if estado_e not in visitados:
            visitados.add(estado_e)
            fila.append((estado_e, acoes + [VIRAR_E]))
        nova_dir_d = (direcao - 1) % 4
        estado_d = (x, y, nova_dir_d)
        if estado_d not in visitados:
            visitados.add(estado_d)
            fila.append((estado_d, acoes + [VIRAR_D]))
    return None


class Agente:
    def __init__(self):
        self.nome = "Agente_Logico_BFS"

        self.x = 1
        self.y = 1
        self.direcao = 0

        self.tem_ouro = False
        self.flechas = 2
        self.wumpus_vivo = True

        self.mapa = {}
        for cx in range(1, 5):
            for cy in range(1, 5):
                self.mapa[(cx, cy)] = "desconhecida"
        self.mapa[(1, 1)] = "segura"
        self.visitadas = {(1, 1)}

        self.candidatos_wumpus = set()
        self.candidatos_buraco = set()
        self.wumpus_confirmado = None

        self.plano = []

        self.brisa_em = set()
        self.cheiro_em = set()
        self.sem_brisa_em = set()
        self.sem_cheiro_em = set()

        self.ouro_pos = None
        self.gold_grabbed = False

        self.ultima_acao = None
        self.tentando_atirar = False
        self.alvo_tiro = None

        self.celulas_descartadas_wumpus = set()

    def atualizar_conhecimento(self, sensores):
        pos = (self.x, self.y)
        self.mapa[pos] = "segura"
        self.visitadas.add(pos)

        if "BRILHO" in sensores:
            self.ouro_pos = pos

        if "OURO" in sensores:
            self.tem_ouro = True
            self.gold_grabbed = True

        if "GRITO" in sensores:
            self.wumpus_vivo = False
            self.wumpus_confirmado = None
            self.candidatos_wumpus.clear()
            self._recalcular_seguranca()

        if self.ultima_acao == ATIRAR and "GRITO" not in sensores and self.wumpus_vivo:
            tx = self.x + DX[self.direcao]
            ty = self.y + DY[self.direcao]
            if 1 <= tx <= 4 and 1 <= ty <= 4:
                self.celulas_descartadas_wumpus.add((tx, ty))
                self.candidatos_wumpus.discard((tx, ty))
                if self.wumpus_confirmado == (tx, ty):
                    self.wumpus_confirmado = None
                if len(self.candidatos_wumpus) == 1:
                    self.wumpus_confirmado = next(iter(self.candidatos_wumpus))
                    self.mapa[self.wumpus_confirmado] = "perigosa"

        if "BRISA" in sensores:
            self.brisa_em.add(pos)
        else:
            self.sem_brisa_em.add(pos)

        if "CHEIRO" in sensores:
            self.cheiro_em.add(pos)
        else:
            self.sem_cheiro_em.add(pos)

        self._inferir_wumpus()
        self._inferir_buracos()
        self._marcar_seguros()

    def _inferir_wumpus(self):
        if not self.wumpus_vivo:
            self.candidatos_wumpus.clear()
            return

        novos_candidatos = set()
        for pos in self.cheiro_em:
            adj = celulas_adjacentes(pos[0], pos[1])
            for c in adj:
                if self.mapa[c] != "segura":
                    novos_candidatos.add(c)

        for pos in self.sem_cheiro_em:
            adj = set(celulas_adjacentes(pos[0], pos[1]))
            novos_candidatos -= adj

        novos_candidatos -= self.candidatos_buraco
        novos_candidatos -= self.celulas_descartadas_wumpus

        self.candidatos_wumpus = novos_candidatos

        if len(self.candidatos_wumpus) == 1:
            self.wumpus_confirmado = next(iter(self.candidatos_wumpus))
            self.mapa[self.wumpus_confirmado] = "perigosa"

    def _inferir_buracos(self):
        if not self.brisa_em:
            return

        candidatos = None
        for pos in self.brisa_em:
            adj = set(c for c in celulas_adjacentes(pos[0], pos[1]) if c not in self.visitadas)
            if candidatos is None:
                candidatos = adj
            else:
                candidatos &= adj

        if candidatos is None:
            return

        for pos in self.sem_brisa_em:
            adj = set(celulas_adjacentes(pos[0], pos[1]))
            candidatos -= adj

        if self.wumpus_vivo:
            candidatos -= self.candidatos_wumpus
            if self.wumpus_confirmado:
                candidatos.discard(self.wumpus_confirmado)

        self.candidatos_buraco = candidatos
        for c in candidatos:
            self.mapa[c] = "perigosa"

    def _marcar_seguros(self):
        sem_buraco = set()
        for pos in self.sem_brisa_em:
            for adj in celulas_adjacentes(pos[0], pos[1]):
                sem_buraco.add(adj)
        sem_buraco |= self.visitadas

        if not self.wumpus_vivo:
            sem_wumpus = {(cx, cy) for cx in range(1, 5) for cy in range(1, 5)}
        else:
            sem_wumpus = set()
            for pos in self.sem_cheiro_em:
                for adj in celulas_adjacentes(pos[0], pos[1]):
                    sem_wumpus.add(adj)
            sem_wumpus |= self.visitadas
            for c in self.celulas_descartadas_wumpus:
                sem_wumpus.add(c)

        for cx in range(1, 5):
            for cy in range(1, 5):
                c = (cx, cy)
                if c in sem_buraco and c in sem_wumpus:
                    if c not in self.candidatos_buraco:
                        self.mapa[c] = "segura"

    def _recalcular_seguranca(self):
        self._inferir_buracos()
        for cx in range(1, 5):
            for cy in range(1, 5):
                c = (cx, cy)
                if c not in self.candidatos_buraco:
                    self.mapa[c] = "segura"

    def celulas_seguras(self):
        return {c for c, v in self.mapa.items() if v == "segura"}

    def fronteira_nao_visitada(self):
        fronteira = set()
        for vis in self.visitadas:
            for adj in celulas_adjacentes(vis[0], vis[1]):
                if adj not in self.visitadas and self.mapa[adj] == "segura":
                    fronteira.add(adj)
        return fronteira

    def planejar_ir_para(self, destino):
        seguras = self.celulas_seguras()
        seguras.add((self.x, self.y))
        return bfs_caminho((self.x, self.y), destino, seguras, self.direcao)

    def melhor_destino_exploracao(self):
        fronteira = self.fronteira_nao_visitada()
        if fronteira:
            return min(fronteira, key=lambda c: abs(c[0] - self.x) + abs(c[1] - self.y))
        nao_visitadas = {c for c, v in self.mapa.items() if v == "segura" and c not in self.visitadas}
        if nao_visitadas:
            return min(nao_visitadas, key=lambda c: abs(c[0] - self.x) + abs(c[1] - self.y))
        return None

    def tentar_atirar_wumpus(self):
        if not self.wumpus_vivo or self.wumpus_confirmado is None or self.flechas <= 0:
            return False

        wx, wy = self.wumpus_confirmado
        seguras = self.celulas_seguras()

        posicoes_tiro = []
        for dir_tiro in range(4):
            fx = wx - DX[dir_tiro]
            fy = wy - DY[dir_tiro]
            if 1 <= fx <= 4 and 1 <= fy <= 4 and (fx, fy) in seguras:
                posicoes_tiro.append(((fx, fy), dir_tiro))

        if not posicoes_tiro:
            return False

        posicoes_tiro.sort(key=lambda pt: abs(pt[0][0] - self.x) + abs(pt[0][1] - self.y))
        pos_tiro, dir_necessaria = posicoes_tiro[0]

        plano_movimento = bfs_caminho((self.x, self.y), pos_tiro, seguras, self.direcao)
        if plano_movimento is None:
            return False

        dir_final = self.direcao
        for acao in plano_movimento:
            if acao == VIRAR_E:
                dir_final = (dir_final + 1) % 4
            elif acao == VIRAR_D:
                dir_final = (dir_final - 1) % 4

        viradas = []
        while dir_final != dir_necessaria:
            viradas.append(VIRAR_E)
            dir_final = (dir_final + 1) % 4

        self.plano = plano_movimento + viradas + [ATIRAR]
        self.tentando_atirar = True
        return True

    def validar_plano(self):
        if not self.plano:
            return
        x, y, d = self.x, self.y, self.direcao
        for acao in self.plano:
            if acao == MOVER:
                nx, ny = x + DX[d], y + DY[d]
                if self.mapa.get((nx, ny)) == "perigosa":
                    self.plano = []
                    return
                x, y = nx, ny
            elif acao == VIRAR_E:
                d = (d + 1) % 4
            elif acao == VIRAR_D:
                d = (d - 1) % 4

    def executar_acao(self, acao):
        if acao == MOVER:
            nx = self.x + DX[self.direcao]
            ny = self.y + DY[self.direcao]
            if 1 <= nx <= 4 and 1 <= ny <= 4:
                self.x, self.y = nx, ny
        elif acao == VIRAR_E:
            self.direcao = (self.direcao + 1) % 4
        elif acao == VIRAR_D:
            self.direcao = (self.direcao - 1) % 4
        elif acao == ATIRAR:
            if self.flechas > 0:
                self.flechas -= 1
            self.tentando_atirar = False
        self.ultima_acao = acao

    def tomar_decisao(self, sensores):
        if "CHOQUE" in sensores:
            self.plano = []

        self.atualizar_conhecimento(sensores)
        self.validar_plano()

        if self.tem_ouro:
            if (self.x, self.y) == (1, 1):
                return ESCALAR
            if not self.plano:
                self.plano = self.planejar_ir_para((1, 1))
                if self.plano is None:
                    self.plano = []
            if self.plano:
                acao = self.plano.pop(0)
                self.executar_acao(acao)
                return acao

        if "BRILHO" in sensores and not self.tem_ouro:
            self.plano = []
            self.executar_acao(AGARRAR)
            return AGARRAR

        if self.plano:
            acao = self.plano.pop(0)
            self.executar_acao(acao)
            return acao

        if self.wumpus_confirmado and self.wumpus_vivo and self.flechas > 0:
            if self.tentar_atirar_wumpus():
                acao = self.plano.pop(0)
                self.executar_acao(acao)
                return acao

        destino = self.melhor_destino_exploracao()
        if destino:
            plano = self.planejar_ir_para(destino)
            if plano is not None:
                self.plano = plano
                if self.plano:
                    acao = self.plano.pop(0)
                    self.executar_acao(acao)
                    return acao

        if self.wumpus_vivo and self.candidatos_wumpus and self.flechas > 0:
            seguras = self.celulas_seguras()
            for cand in self.candidatos_wumpus:
                if cand in self.celulas_descartadas_wumpus:
                    continue
                wx, wy = cand
                for dir_tiro in range(4):
                    fx = wx - DX[dir_tiro]
                    fy = wy - DY[dir_tiro]
                    alvo = (fx + DX[dir_tiro], fy + DY[dir_tiro])
                    if alvo in self.celulas_descartadas_wumpus:
                        continue
                    if 1 <= fx <= 4 and 1 <= fy <= 4 and (fx, fy) in seguras:
                        plano_tiro = bfs_caminho((self.x, self.y), (fx, fy), seguras, self.direcao)
                        if plano_tiro is not None:
                            dir_final = self.direcao
                            for a in plano_tiro:
                                if a == VIRAR_E: dir_final = (dir_final + 1) % 4
                                elif a == VIRAR_D: dir_final = (dir_final - 1) % 4
                            viradas = []
                            d = dir_final
                            while d != dir_tiro:
                                viradas.append(VIRAR_E)
                                d = (d + 1) % 4
                            self.plano = plano_tiro + viradas + [ATIRAR]
                            acao = self.plano.pop(0)
                            self.executar_acao(acao)
                            return acao

        desconhecidas = [(c, v) for c, v in self.mapa.items() if v == "desconhecida"]
        if desconhecidas:
            seguras_atual = self.celulas_seguras()
            candidatas = []
            for c, _ in desconhecidas:
                adj_vis = [a for a in celulas_adjacentes(c[0], c[1]) if a in self.visitadas]
                if adj_vis:
                    score = 0
                    if c in self.candidatos_buraco: score += 10
                    if c in self.candidatos_wumpus: score += 10
                    candidatas.append((score, c))
            if candidatas:
                candidatas.sort()
                score_melhor, destino_arriscado = candidatas[0]
                if score_melhor == 0:
                    seguras_com_destino = seguras_atual | {destino_arriscado}
                    plano = bfs_caminho((self.x, self.y), destino_arriscado,
                                        seguras_com_destino, self.direcao)
                    if plano is not None:
                        self.plano = plano
                        if self.plano:
                            acao = self.plano.pop(0)
                            self.executar_acao(acao)
                            return acao

        if (self.x, self.y) == (1, 1):
            return ESCALAR

        plano_saida = self.planejar_ir_para((1, 1))
        if plano_saida:
            self.plano = plano_saida
            acao = self.plano.pop(0)
            self.executar_acao(acao)
            return acao

        self.executar_acao(VIRAR_E)
        return VIRAR_E

        # =================================================================
        # FIM DA LÓGICA DO AGENTE
        # =================================================================


# =====================================================================
# SISTEMA DE AVALIAÇÃO E CHAVEAMENTO (NÃO MODIFICAR ABAIXO)
# =====================================================================

def modo_master():
    agente = Agente()
    print(agente.nome, flush=True)
    while True:
        linha = sys.stdin.readline()
        if not linha:
            break
        linha = linha.strip()
        sensores = linha.split(',') if linha != "NADA" else []
        acao = agente.tomar_decisao(sensores)
        print(acao, flush=True)


def carregar_mundo_stdin():
    linhas = []
    for _ in range(4):
        linha = sys.stdin.readline()
        if not linha:
            break
        linhas.append(linha.strip().split())

    if len(linhas) < 4:
        return None

    mundo = {'wumpus': None, 'buraco': None, 'ouro': None, 'wumpus_vivo': True}
    for r in range(4):
        for c in range(4):
            val = linhas[r][c]
            x, y = c + 1, 4 - r
            if val == '#':
                mundo['wumpus'] = (x, y)
            elif val == '*':
                mundo['buraco'] = (x, y)
            elif val == '$':
                mundo['ouro'] = (x, y)
            elif val == '@':
                mundo['saida'] = (x, y)

    if mundo['ouro'] is None and mundo['wumpus'] is not None:
        mundo['ouro'] = mundo['wumpus']
    return mundo


def modo_judge_interno():
    mundo = carregar_mundo_stdin()
    if not mundo:
        print("FRACASSO")
        return

    agente = Agente()
    x, y = 1, 1
    direcao = 0
    dx, dy = [1, 0, -1, 0], [0, 1, 0, -1]

    flechas = 2
    tem_ouro = False
    jogo_ativo = True
    resultado_final = "FRACASSO"

    bateu_parede = False
    gritou = False
    pegou_ouro = False
    erro_escada = False
    entrou_sala_ouro = False

    turnos = 0
    while jogo_ativo and turnos < 500:
        turnos += 1

        if (x, y) == mundo['wumpus'] and mundo['wumpus_vivo']:
            break
        if (x, y) == mundo['buraco']:
            break

        sensores = []
        adjacentes = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        if mundo['buraco'] in adjacentes:
            sensores.append("BRISA")
        if mundo['wumpus_vivo'] and mundo['wumpus'] in adjacentes:
            sensores.append("CHEIRO")
        if entrou_sala_ouro:
            sensores.append("BRILHO")
            entrou_sala_ouro = False
        if bateu_parede:
            sensores.append("CHOQUE")
            bateu_parede = False
        if gritou:
            sensores.append("GRITO")
            gritou = False
        if pegou_ouro:
            sensores.append("OURO")
            pegou_ouro = False
        if erro_escada:
            sensores.append("NO ESCADA")
            erro_escada = False

        acao = agente.tomar_decisao(sensores)

        if acao == MOVER:
            nx, ny = x + dx[direcao], y + dy[direcao]
            if 1 <= nx <= 4 and 1 <= ny <= 4:
                x, y = nx, ny
                if (x, y) == mundo['ouro'] and not tem_ouro:
                    entrou_sala_ouro = True
            else:
                bateu_parede = True
        elif acao == VIRAR_E:
            direcao = (direcao + 1) % 4
        elif acao == VIRAR_D:
            direcao = (direcao - 1) % 4
        elif acao == ATIRAR:
            if flechas > 0:
                flechas -= 1
                tx, ty = x + dx[direcao], y + dy[direcao]
                if (tx, ty) == mundo['wumpus'] and mundo['wumpus_vivo']:
                    mundo['wumpus_vivo'] = False
                    gritou = True
        elif acao == AGARRAR:
            if (x, y) == mundo['ouro'] and not tem_ouro:
                tem_ouro = True
                pegou_ouro = True
        elif acao == ESCALAR:
            if (x, y) == (1, 1):
                if tem_ouro:
                    resultado_final = "SUCESSO"
                    jogo_ativo = False
                else:
                    erro_escada = True

    print(resultado_final)


if __name__ == "__main__":
    if "--master" in sys.argv:
        modo_master()
    else:
        modo_judge_interno()