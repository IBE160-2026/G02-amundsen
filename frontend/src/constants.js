// Må holdes i samsvar med MAX_CV_LENGTH/MAX_JOB_AD_LENGTH i
// backend/app/models.py. Frontenden kan ikke importere disse direkte fra
// Python-koden, så de dupliseres bevisst her som en enkel klientside-grense
// (serveren validerer uansett på nytt – dette er bare for å gi tidlig,
// forståelig tilbakemelding i grensesnittet).
export const MAX_CV_LENGTH = 20_000
export const MAX_JOB_AD_LENGTH = 10_000
