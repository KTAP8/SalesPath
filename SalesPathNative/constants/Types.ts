export type SalesMan = {
  SalesName: string;
};
export type Client = {
  ClientId: string;
  ClientReg: string;
  ClientSubReg: string;
  ClientType: string;
  SalesName: string;
};

export type Visit = {
  VisitId: number;
  SalesName: string;
  ClientId: string;
  VisitDateTime: string;
  Activity: string;
  Notes: string;
  ProblemNotes?: string;
  Resolved: boolean;
  InvoiceAmount?: number;
};
