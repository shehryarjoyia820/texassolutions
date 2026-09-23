/* Texas Solutions Truck Dispatch: the 11 extra free calculators (Tools hub). */
(function () {
  'use strict';
  var $ = function (id) { return document.getElementById(id); };
  var num = function (id) { var el = $(id); if (!el) return 0; var x = parseFloat(el.value); return isFinite(x) ? x : 0; };
  var money = function (n, d) {
    if (!isFinite(n)) n = 0;
    return '$' + n.toLocaleString('en-US', { minimumFractionDigits: d || 0, maximumFractionDigits: d || 0 });
  };
  var pctStr = function (n) { return (isFinite(n) ? n.toFixed(1) : '0.0') + '%'; };
  var on = function (ids, evt, fn) {
    for (var i = 0; i < ids.length; i++) { var el = $(ids[i]); if (el) el.addEventListener(evt, fn); }
  };

  /* -------------------------------------------------- Cost Per Mile */
  if ($('cpmCalc')) {
    var cpmIds = ['cpmPayment', 'cpmInsurance', 'cpmPermits', 'cpmOtherFixed', 'cpmFuel', 'cpmMaint', 'cpmDriverPay', 'cpmMiles'];
    function cpmRun() {
      var fixed = num('cpmPayment') + num('cpmInsurance') + num('cpmPermits') + num('cpmOtherFixed');
      var varMi = num('cpmFuel') + num('cpmMaint') + num('cpmDriverPay');
      var miles = Math.max(1, num('cpmMiles'));
      var fixedPerMi = fixed / miles;
      var cpm = fixedPerMi + varMi;
      $('cpmBig').innerHTML = '$' + cpm.toFixed(2) + '<small>per mile, all-in</small>';
      $('cpmFixedTotal').textContent = money(fixed);
      $('cpmFixedPerMi').textContent = '$' + fixedPerMi.toFixed(2) + ' /mi';
      $('cpmVarPerMi').textContent = '$' + varMi.toFixed(2) + ' /mi';
      $('cpmMonthlyTotal').textContent = money(cpm * miles);
    }
    on(cpmIds, 'input', cpmRun); cpmRun();
  }

  /* -------------------------------------------------- Load Profitability */
  if ($('lpCalc')) {
    var lpIds = ['lpRate', 'lpLoaded', 'lpDeadhead', 'lpOther', 'lpCpm'];
    function lpRun() {
      var rate = num('lpRate'), loaded = Math.max(0, num('lpLoaded')), dead = Math.max(0, num('lpDeadhead'));
      var totalMi = loaded + dead, cpm = num('lpCpm'), other = num('lpOther');
      var totalCost = cpm * totalMi + other;
      var net = rate - totalCost;
      var margin = rate > 0 ? (net / rate * 100) : 0;
      $('lpBig').innerHTML = money(net) + '<small>net profit</small>';
      $('lpBig').style.color = net < 0 ? '#ff8a73' : '';
      $('lpTotalMi').textContent = totalMi.toLocaleString('en-US') + ' mi';
      $('lpTotalCost').textContent = money(totalCost);
      $('lpMargin').textContent = pctStr(margin);
      $('lpRatePerLoaded').textContent = loaded ? '$' + (rate / loaded).toFixed(2) + ' /mi' : '-';
      $('lpRatePerTotal').textContent = totalMi ? '$' + (rate / totalMi).toFixed(2) + ' /mi' : '-';
    }
    on(lpIds, 'input', lpRun); lpRun();
  }

  /* -------------------------------------------------- Break-Even */
  if ($('beCalc')) {
    var beIds = ['beFixed', 'beVar', 'beRate', 'beMiles'];
    function beRun() {
      var fixed = num('beFixed'), varMi = num('beVar'), rate = num('beRate'), planned = num('beMiles');
      var contribution = rate - varMi;
      var warn = $('beWarn');
      if (contribution <= 0) {
        warn.style.display = 'block';
        $('beBig').innerHTML = '&#8734;<small>miles / month</small>';
        $('beWeekly').textContent = '-'; $('beMargin').textContent = '$' + contribution.toFixed(2) + ' /mi';
        $('bePlannedProfit').textContent = money((contribution * planned) - fixed);
        return;
      }
      warn.style.display = 'none';
      var beMonthly = fixed / contribution;
      $('beBig').innerHTML = Math.round(beMonthly).toLocaleString('en-US') + '<small>miles / month</small>';
      $('beWeekly').textContent = Math.round(beMonthly / 4.33).toLocaleString('en-US') + ' mi/wk';
      $('beMargin').textContent = '$' + contribution.toFixed(2) + ' /mi';
      var plannedProfit = (contribution * planned) - fixed;
      $('bePlannedProfit').textContent = money(plannedProfit);
    }
    on(beIds, 'input', beRun); beRun();
  }

  /* -------------------------------------------------- Deadhead Miles */
  if ($('dhCalc')) {
    var dhIds = ['dhLoaded', 'dhDead', 'dhRevenue', 'dhCpm'];
    function dhRun() {
      var loaded = Math.max(0, num('dhLoaded')), dead = Math.max(0, num('dhDead')), rev = num('dhRevenue');
      var total = loaded + dead;
      var pct = total ? (dead / total * 100) : 0;
      var quoted = loaded ? rev / loaded : 0;
      var effective = total ? rev / total : 0;
      $('dhBig').innerHTML = pct.toFixed(1) + '%<small>deadhead miles</small>';
      $('dhTotalMi').textContent = total.toLocaleString('en-US') + ' mi';
      $('dhQuoted').textContent = '$' + quoted.toFixed(2) + ' /mi';
      $('dhEffective').textContent = '$' + effective.toFixed(2) + ' /mi';
      $('dhLost').textContent = '$' + Math.max(0, quoted - effective).toFixed(2) + ' /mi';
      var cpm = num('dhCpm'), row = $('dhProfitRow');
      if (cpm > 0) {
        row.style.display = ''; $('dhProfit').textContent = money(rev - cpm * total);
      } else { row.style.display = 'none'; }
    }
    on(dhIds, 'input', dhRun); dhRun();
  }

  /* -------------------------------------------------- Driver Pay */
  if ($('dpCalc')) {
    var dpModelIds = ['dpRateMile', 'dpMilesWk', 'dpPayLoad', 'dpLoadsWk', 'dpGrossWk', 'dpPct', 'dpHourly', 'dpHoursWk', 'dpWeeks'];
    function dpModel() { var c = document.querySelector('input[name=dpModel]:checked'); return c ? c.value : 'mile'; }
    function dpShowGroup() {
      var m = dpModel();
      var groups = document.querySelectorAll('#dpCalc .dp-group');
      for (var i = 0; i < groups.length; i++) groups[i].style.display = (groups[i].getAttribute('data-model') === m) ? '' : 'none';
    }
    function dpRun() {
      var m = dpModel(), weekly = 0;
      if (m === 'mile') weekly = num('dpRateMile') * num('dpMilesWk');
      else if (m === 'load') weekly = num('dpPayLoad') * num('dpLoadsWk');
      else if (m === 'pct') weekly = num('dpGrossWk') * num('dpPct') / 100;
      else if (m === 'hour') weekly = num('dpHourly') * num('dpHoursWk');
      var weeks = Math.max(1, Math.min(52, num('dpWeeks')));
      $('dpBig').innerHTML = money(weekly) + '<small>per week</small>';
      $('dpMonthly').textContent = money(weekly * 4.33);
      $('dpAnnual').textContent = money(weekly * weeks);
    }
    Array.prototype.forEach.call(document.querySelectorAll('input[name=dpModel]'), function (r) {
      r.addEventListener('change', function () { dpShowGroup(); dpRun(); });
    });
    on(dpModelIds, 'input', dpRun);
    dpShowGroup(); dpRun();
  }

  /* -------------------------------------------------- IFTA Mileage */
  var ifta = $('iftaCalc');
  if (ifta) {
    var iftaStates = [];
    try { iftaStates = JSON.parse(ifta.getAttribute('data-states')); } catch (e) { iftaStates = ['Texas']; }
    var iftaRows = $('iftaRows');
    var stateOpts = iftaStates.map(function (s) { return '<option>' + s + '</option>'; }).join('');
    function iftaRowHtml() {
      return '<tr>' +
        '<td><select class="ifta-state">' + stateOpts + '</select></td>' +
        '<td><input type="number" class="ifta-miles" min="0" step="1" value="0" inputmode="numeric"></td>' +
        '<td><input type="number" class="ifta-purchased" min="0" step="1" value="0" inputmode="numeric"></td>' +
        '<td><input type="number" class="ifta-rate" min="0" step="0.001" placeholder="optional" inputmode="decimal"></td>' +
        '<td><button type="button" class="ifta-rm" aria-label="Remove row">&times;</button></td>' +
        '</tr>';
    }
    function iftaAddRow(stateIndex) {
      var tr = document.createElement('tbody');
      tr.innerHTML = iftaRowHtml();
      var row = tr.firstElementChild;
      if (typeof stateIndex === 'number' && row.querySelector('.ifta-state').options[stateIndex]) {
        row.querySelector('.ifta-state').selectedIndex = stateIndex;
      }
      iftaRows.appendChild(row);
    }
    function iftaRun() {
      var mpg = Math.max(0.1, num('iftaMpg'));
      var rows = iftaRows.querySelectorAll('tr');
      var totalMiles = 0, totalConsumed = 0, totalPurchased = 0, totalTax = 0, anyRate = false;
      for (var i = 0; i < rows.length; i++) {
        var r = rows[i];
        var miles = parseFloat(r.querySelector('.ifta-miles').value) || 0;
        var purchased = parseFloat(r.querySelector('.ifta-purchased').value) || 0;
        var rate = parseFloat(r.querySelector('.ifta-rate').value) || 0;
        var consumed = miles / mpg;
        var net = consumed - purchased;
        totalMiles += miles; totalConsumed += consumed; totalPurchased += purchased;
        if (rate > 0) { anyRate = true; totalTax += net * rate; }
      }
      $('iftaTotalMiles').textContent = Math.round(totalMiles).toLocaleString('en-US');
      $('iftaTotalPurchased').textContent = totalPurchased.toFixed(1);
      var netGal = totalConsumed - totalPurchased;
      $('iftaBig').innerHTML = netGal.toFixed(1) + '<small>net taxable gallons</small>';
      $('iftaMi').textContent = Math.round(totalMiles).toLocaleString('en-US') + ' mi';
      $('iftaConsumed').textContent = totalConsumed.toFixed(1) + ' gal';
      $('iftaPurchased').textContent = totalPurchased.toFixed(1) + ' gal';
      $('iftaTax').textContent = anyRate ? money(totalTax, 2) : 'Add a rate per row to estimate';
    }
    iftaRows.addEventListener('input', iftaRun);
    iftaRows.addEventListener('change', iftaRun);
    iftaRows.addEventListener('click', function (e) {
      if (e.target.classList.contains('ifta-rm')) {
        if (iftaRows.querySelectorAll('tr').length > 1) { e.target.closest('tr').remove(); iftaRun(); }
      }
    });
    $('iftaAddRow').addEventListener('click', function () { iftaAddRow(); iftaRun(); });
    $('iftaMpg').addEventListener('input', iftaRun);
    // Seed with one row (Texas if present) so the table isn't empty on load.
    var txIndex = iftaStates.indexOf('Texas');
    iftaAddRow(txIndex >= 0 ? txIndex : 0);
    iftaRun();
  }

  /* -------------------------------------------------- Per Diem */
  if ($('pdCalc')) {
    var pdIds = ['pdDays', 'pdRate', 'pdDeductPct', 'pdTaxRate'];
    function pdRun() {
      var total = Math.max(0, num('pdDays')) * Math.max(0, num('pdRate'));
      var deductible = total * (num('pdDeductPct') / 100);
      var savings = deductible * (num('pdTaxRate') / 100);
      $('pdBig').innerHTML = money(total) + '<small>total per diem, per year</small>';
      $('pdDeductible').textContent = money(deductible);
      $('pdSavings').textContent = money(savings);
    }
    on(pdIds, 'input', pdRun); pdRun();
  }

  /* -------------------------------------------------- Truck Loan */
  if ($('tlCalc')) {
    var tlIds = ['tlPrice', 'tlDown', 'tlRate', 'tlTerm'];
    function tlRun() {
      var financed = Math.max(0, num('tlPrice') - num('tlDown'));
      var n = Math.max(1, Math.round(num('tlTerm')));
      var r = (num('tlRate') / 100) / 12;
      var payment;
      if (r <= 0) payment = financed / n;
      else payment = financed * (r * Math.pow(1 + r, n)) / (Math.pow(1 + r, n) - 1);
      if (!isFinite(payment)) payment = 0;
      var total = payment * n;
      $('tlBig').innerHTML = money(payment, 2) + '<small>per month</small>';
      $('tlFinanced').textContent = money(financed);
      $('tlTotal').textContent = money(total);
      $('tlInterest').textContent = money(Math.max(0, total - financed));
    }
    on(tlIds, 'input', tlRun); tlRun();
  }

  /* -------------------------------------------------- Maintenance Budget */
  if ($('mbCalc')) {
    var mbIds = ['mbAge', 'mbMiles', 'mbCustom'];
    function mbBracketRate(age) {
      if (age <= 2) return 0.12;
      if (age <= 5) return 0.18;
      if (age <= 8) return 0.25;
      return 0.35;
    }
    function mbRun() {
      var age = Math.max(0, num('mbAge')), miles = Math.max(0, num('mbMiles')), custom = num('mbCustom');
      var rate = custom > 0 ? custom : mbBracketRate(age);
      var annual = rate * miles;
      $('mbBig').innerHTML = money(annual) + '<small>per year</small>';
      $('mbRate').textContent = '$' + rate.toFixed(2) + ' /mi' + (custom > 0 ? ' (your rate)' : ' (age-based)');
      $('mbMonthly').textContent = money(annual / 12);
      $('mbWeekly').textContent = money(annual / 52);
    }
    on(mbIds, 'input', mbRun); mbRun();
  }

  /* -------------------------------------------------- Hours of Service */
  if ($('hosCalc')) {
    var hosIds = ['hosDriven', 'hosOnDuty', 'hosElapsed', 'hosCycleUsed'];
    function hosRun() {
      var driven = num('hosDriven'), onDuty = num('hosOnDuty'), elapsed = num('hosElapsed');
      var cycleLimit = parseFloat($('hosCycleType').value) || 70;
      var cycleUsed = num('hosCycleUsed');
      var driveLeft = Math.max(0, 11 - driven);
      var windowLeft = Math.max(0, 14 - elapsed);
      var cycleLeft = Math.max(0, cycleLimit - cycleUsed - driven - onDuty);
      var binding = Math.min(driveLeft, windowLeft, cycleLeft);
      var which = 'the 11-hour drive-time limit';
      if (windowLeft === binding && windowLeft <= driveLeft && windowLeft <= cycleLeft) which = 'the 14-hour on-duty window';
      else if (cycleLeft === binding && cycleLeft <= driveLeft && cycleLeft <= windowLeft) which = 'your ' + cycleLimit + '-hour cycle limit';
      $('hosBig').innerHTML = binding.toFixed(1) + '<small>more hours today</small>';
      $('hosDriveLeft').textContent = driveLeft.toFixed(1) + ' hr';
      $('hosWindowLeft').textContent = windowLeft.toFixed(1) + ' hr';
      $('hosCycleLeft').textContent = cycleLeft.toFixed(1) + ' hr';
      $('hosBinding').textContent = binding <= 0 ? 'None left — go off duty' : which;
    }
    on(hosIds, 'input', hosRun);
    $('hosCycleType').addEventListener('change', hosRun);
    hosRun();
  }

  /* -------------------------------------------------- Freight Class */
  if ($('fcCalc')) {
    var fcIds = ['fcL', 'fcW', 'fcH', 'fcWeight', 'fcUnits'];
    function fcClassFor(pcf) {
      if (pcf >= 50) return '50';
      if (pcf >= 35) return '55';
      if (pcf >= 30) return '60';
      if (pcf >= 22.5) return '65';
      if (pcf >= 15) return '70';
      if (pcf >= 12) return '77.5';
      if (pcf >= 10) return '85';
      if (pcf >= 8) return '92.5';
      if (pcf >= 6) return '100';
      if (pcf >= 4) return '125';
      if (pcf >= 2) return '150';
      if (pcf >= 1) return '175';
      return '250+';
    }
    function fcRun() {
      var L = Math.max(0.1, num('fcL')), W = Math.max(0.1, num('fcW')), H = Math.max(0.1, num('fcH'));
      var wt = Math.max(0, num('fcWeight')), units = Math.max(1, Math.round(num('fcUnits')));
      var cubePerUnit = (L * W * H) / 1728;
      var totalCube = cubePerUnit * units;
      var totalWeight = wt * units;
      var density = totalCube > 0 ? (totalWeight / totalCube) : 0;
      $('fcClass').textContent = 'Class ' + fcClassFor(density);
      $('fcDensity').textContent = density.toFixed(1) + ' lb/ft³';
      $('fcCube').textContent = totalCube.toFixed(1) + ' ft³';
      $('fcTotalWeight').textContent = totalWeight.toLocaleString('en-US') + ' lbs';
    }
    on(fcIds, 'input', fcRun); fcRun();
  }
})();
