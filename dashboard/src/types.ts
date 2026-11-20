// Tipos que reflejan las respuestas de la API (/api/...)

export interface Kpis {
  jugadas: { dropbacks: number; partidos: number; analizadas: number }
  supervivencia: { supervivencia_2_5s: number; mediana_colapso_s: number | null }
  engano: {
    pct_fallido_con_engano: number | null
    pct_fallido_sin_engano: number | null
    n_con_engano: number
    n_sin_engano: number
  }
  ruptura: {
    pct_ruptura: number | null
    pct_sack_con_colapso: number | null
    pct_sack_sin_colapso: number | null
    n_con_colapso: number
  }
}

export interface PassRusher {
  nflId: number
  displayName: string | null
  officialPosition: string | null
  rush_snaps: number
  rupturas: number
  pct_ruptura: number
  seg_prom_colapso: number | null
  hits: number
  hurries: number
  sacks: number
}
export interface RankingRow {
  defensiveTeam: string
  n_jugadas: number
  disguise_score_prom: number
  n_disfrazadas: number
  pct_exito_engano: number | null
  cobertura_mas_disfrazada: string | null
}

export interface Overview {
  kpis: Kpis
  ranking: RankingRow[]
}

export interface PuntoSupervivencia {
  tiempo_s: number
  supervivencia: number
  n_en_riesgo: number
}

export interface GrupoSupervivencia {
  grupo: string
  n_jugadas: number
  puntos: PuntoSupervivencia[]
}

export interface Supervivencia {
  agrupar_por: AgruparPor
  umbral_s: number
  grupos: GrupoSupervivencia[]
}

export type AgruparPor = 'pff_passCoverage' | 'offenseFormation'

export interface JugadaCatalogo {
  gameId: number
  playId: number
  tipo_muestra: 'alto_disguise' | 'ruptura_rapida'
  defensiveTeam: string
  possessionTeam: string
  pff_passCoverage: string
  offenseFormation: string | null
  passResult: string
  disguise_score: number | null
  safeties_snap: number | null
  safeties_esperados: number | null
  tiempo_observado: number | null
  bolsillo_roto: number | null
  shell_snap: string | null
}

export type Rol = 'balon' | 'qb' | 'pass_rusher' | 'safety' | 'ofensiva' | 'defensiva'

export interface Jugador {
  id: number | null
  nombre: string | null
  camiseta: number | null
  rol: Rol
  posicion: string | null
  x: number
  y: number
  o: number | null
}

export interface Frame {
  frame_rel: number
  tiempo_s: number
  evento: string | null
  jugadores: Jugador[]
}

export interface DetalleJugada extends Omit<JugadaCatalogo, 'bolsillo_roto'> {
  bolsillo_roto: boolean
  frame_ruptura_rel: number | null
  frame_fin_rel: number
  evento_fin: string
  frames: Frame[]
}

