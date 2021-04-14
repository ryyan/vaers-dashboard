const http = require("http");
const fs = require("fs");
const path = require("path");
const csv = require("@fast-csv/parse");

const host = "localhost";
const port = 8000;
const dataFolder = "data";

class VaersData {
  constructor(row) {
    this.vaersId = row.VAERS_ID;
    this.recvDate = row.RECVDATE;
    this.state = row.STATE;
    this.ageYrs = row.AGE_YRS;
    this.cageYr = row.CAGE_YR;
    this.cageMo = row.CAGE_MO;
    this.sex = row.SEX;
    this.rptDate = row.RPT_DATE;
    this.symptomText = row.SYMPTOM_TEXT;
    this.died = row.DIED;
    this.dateDied = row.DATEDIED;
    this.lThread = row.L_THREAT;
    this.erVisit = row.ER_VISIT;
    this.hospital = row.HOSPITAL;
    this.hospitalDays = row.HOSPDAYS;
    this.xStay = row.X_STAY;
    this.disable = row.DISABLE;
    this.recovered = row.RECOVD;
    this.vaxDate = row.VAX_DATE;
    this.onsetDate = row.ONSET_DATE;
    this.numDays = row.NUMDAYS;
    this.labData = row.LAB_DATA;
    this.vAdminBy = row.V_ADMINBY;
    this.vFundBy = row.V_FUNDBY;
    this.otherMeds = row.OTHER_MEDS;
    this.currentlyIll = row.CUR_ILL;
    this.history = row.HISTORY;
    this.priorVax = row.PRIOR_VAX;
    this.spltType = row.SPLTTYPE;
    this.formVersion = row.FORM_VERS;
    this.todaysDate = row.TODAYS_DATE;
    this.birthDefect = row.BIRTH_DEFECT;
    this.officeVisit = row.OFC_VISIT;
    this.erEdVisit = row.ER_ED_VISIT;
    this.allergies = row.ALLERGIES;
  }
}

class SymptomsData {
  constructor(row) {
    this.vaersId = row.VAERS_ID;
    this.symptoms = "";

    if (row.SYMPTOM1) {
      this.symptoms = row.SYMPTOM1;
    }
    if (row.SYMPTOM2) {
      this.symptoms.concat(`, ${row.SYMPTOM2}`);
    }
    if (row.SYMPTOM3) {
      this.symptoms.concat(`, ${row.SYMPTOM3}`);
    }
    if (row.SYMPTOM4) {
      this.symptoms.concat(`, ${row.SYMPTOM4}`);
    }
    if (row.SYMPTOM5) {
      this.symptoms.concat(`, ${row.SYMPTOM5}`);
    }
  }
}

class VaxData {
  constructor(row) {
    this.vaersId = row.VAERS_ID;
    this.vaxType = row.VAX_TYPE;
    this.vaxManufacturer = row.VAX_MANU;
    this.vaxLot = row.VAX_LOT;
    this.vaxDoseSeries = row.VAX_DOSE_SERIES;
    this.vaxRoute = row.VAX_ROUTE;
    this.vaxSite = row.VAX_SITE;
    this.vaxName = row.VAX_NAME;
  }
}

const parse = async function (filepath, dataClass) {
  var results = [];

  fs.createReadStream(path.resolve(filepath))
    .pipe(csv.parse({ headers: true }))
    .on("data", (row) => {
      results.push(new dataClass(row));
    })
    .on("error", (error) => console.error(error))
    .on("end", (rowCount) =>
      console.log(`Parsed ${rowCount} rows from ${filepath}`)
    );

  return results;
};

const parseAll = async function () {
  console.log("Parsing data files");
  var vaersData, symptomsData, vaxData;

  const dir = await fs.promises.readdir(dataFolder);
  for await (const filename of dir) {
    if (filename.endsWith("VAX.csv")) {
      vaxData = parse(`${dataFolder}/${filename}`, VaxData);
    }
    if (filename.endsWith("DATA.csv")) {
      vaersData = parse(`${dataFolder}/${filename}`, VaersData);
    }
    if (filename.endsWith("SYMPTOMS.csv")) {
      symptomsData = parse(`${dataFolder}/${filename}`, SymptomsData);
    }
  }
};

const requestListener = function (request, response) {
  console.log("request ", request.url);

  parseAll();

  response.writeHead(200, { "Content-Type": "application/json" });
  response.end("success!", "utf-8");
  return;
};

const server = http.createServer(requestListener);
server.listen(port, host, () => {
  console.log(`Server is running on http://${host}:${port}`);
});
