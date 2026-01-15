import React from 'react';

const MOROCCAN_STOCKS = [
    { s: 'AFM.MA', n: 'AFMA' }, { s: 'AFI.MA', n: 'Afric Ind.' }, { s: 'GAZ.MA', n: 'Afriquia Gaz' },
    { s: 'AGM.MA', n: 'Agma' }, { s: 'AKT.MA', n: 'Akdital' }, { s: 'ADI.MA', n: 'Alliances' },
    { s: 'ALM.MA', n: 'Aluminium' }, { s: 'ACD.MA', n: 'Aradei' }, { s: 'ATL.MA', n: 'AtlantaSanad' },
    { s: 'ATW.MA', n: 'Attijariwafa' }, { s: 'ATH.MA', n: 'Auto Hall' }, { s: 'NEJ.MA', n: 'Auto Nejma' },
    { s: 'AXC.MA', n: 'Axa Credit' }, { s: 'BAL.MA', n: 'Balima' }, { s: 'BCP.MA', n: 'BCP' },
    { s: 'BOA.MA', n: 'Bank of Africa' }, { s: 'BCE.MA', n: 'BMCE' }, { s: 'BCI.MA', n: 'BMCI' },
    { s: 'SBM.MA', n: 'Boissons Maroc' }, { s: 'CRS.MA', n: 'Cartier Saada' }, { s: 'CDA.MA', n: 'Centrale Danone' },
    { s: 'CIH.MA', n: 'CIH Bank' }, { s: 'CMA.MA', n: 'Ciments Maroc' }, { s: 'COL.MA', n: 'Colorado' },
    { s: 'CMGP.MA', n: 'CMGP' }, { s: 'CMT.MA', n: 'CMT' }, { s: 'CSR.MA', n: 'Cosumar' },
    { s: 'CDM.MA', n: 'Credit Maroc' }, { s: 'CTM.MA', n: 'CTM' }, { s: 'DARI.MA', n: 'Dari Couspate' },
    { s: 'DLM.MA', n: 'Delattre Lev.' }, { s: 'DHO.MA', n: 'Delta Hold.' }, { s: 'DIS.MA', n: 'Diac Salaf' },
    { s: 'DWAY.MA', n: 'Disway' }, { s: 'ADH.MA', n: 'Addoha' }, { s: 'NAKL.MA', n: 'Ennakl' },
    { s: 'EQD.MA', n: 'Eqdom' }, { s: 'FBR.MA', n: 'Fenie Bros.' }, { s: 'HPS.MA', n: 'HPS' },
    { s: 'IBMC.MA', n: 'IB Maroc' }, { s: 'IMO.MA', n: 'Immorente' }, { s: 'INV.MA', n: 'Involys' },
    { s: 'IAM.MA', n: 'Maroc Telecom' }, { s: 'JET.MA', n: 'Jet Contr.' }, { s: 'LBV.MA', n: 'Label Vie' },
    { s: 'LHM.MA', n: 'LafargeHolcim' }, { s: 'OULM.MA', n: 'Oulmes' }, { s: 'LES.MA', n: 'Lesieur' },
    { s: 'LYD.MA', n: 'Lydec' }, { s: 'M2M.MA', n: 'M2M Group' }, { s: 'MOX.MA', n: 'Maghreb Oxy.' },
    { s: 'MAB.MA', n: 'Maghrebail' }, { s: 'MNG.MA', n: 'Managem' }, { s: 'ML.MA', n: 'Maroc Leasing' },
    { s: 'MED.MA', n: 'Med Paper' }, { s: 'MIC.MA', n: 'Microdata' }, { s: 'SAL.MA', n: 'Salafin' },
    { s: 'SPPM.MA', n: 'Prom Pharm.' }, { s: 'SOT.MA', n: 'Sothema' }, { s: 'SNLE.MA', n: 'SNEP' },
    { s: 'MSA.MA', n: 'Marsa Maroc' }, { s: 'SONA.MA', n: 'Sonasid' }, { s: 'SNA.MA', n: 'Stokvis' },
    { s: 'STR.MA', n: 'Stroc Ind.' }, { s: 'TQM.MA', n: 'Taqa Morocco' }, { s: 'TMA.MA', n: 'TotalEnergies' },
    { s: 'TGC.MA', n: 'TGCC' }, { s: 'WAA.MA', n: 'Wafa Assur.' }, { s: 'ZEL.MA', n: 'Zellidja' }
];

interface Props {
    currentSymbol: string;
    onSelect: (symbol: string) => void;
}

export function MoroccanStocksList({ currentSymbol, onSelect }: Props) {
    return (
        <div className="flex-1 overflow-hidden flex flex-col mt-4">
            <h3 className="text-slate-400 font-bold mb-2 text-sm flex items-center gap-2">
                <span className="text-red-500">🇲🇦</span> Moroccan Stocks
            </h3>
            <div className="flex-1 overflow-y-auto space-y-1 pr-2 scrollbar-thin scrollbar-thumb-slate-700">
                {MOROCCAN_STOCKS.map(({ s, n }) => (
                    <div key={s}
                        onClick={() => onSelect(s)}
                        className={`p-2 rounded cursor-pointer text-sm flex justify-between items-center ${currentSymbol === s ? 'bg-blue-900/50 text-blue-200 border border-blue-800' : 'hover:bg-slate-800 text-slate-300'}`}>
                        <span className="font-mono font-bold">{n}</span>
                        <span className="text-[10px] opacity-50">{s.replace('.MA', '')}</span>
                    </div>
                ))}
            </div>
        </div>
    );
}
