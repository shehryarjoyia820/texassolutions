/* Texas Solutions Truck Dispatch: the free calculators on the Tools hub.
   Each one registers with TS.tool (js/site.js), which handles input checks,
   "Enter your details", reset/print/save/share and GA4 tool events, and
   calls run() only when every visible input is valid. Formulas are written
   out on each tool page and in docs/HANDOVER.md. */
(function () {
  'use strict';
  var TS = window.TS;
  if (!TS) return;
  var $ = function (id) { return document.getElementById(id); };
  var num = TS.num, money = TS.money;
  var per = function (n) { return '$' + n.toFixed(2) + ' /mi'; };
  var pctStr = function (n) { return (isFinite(n) ? n.toFixed(1) : '0.0') + '%'; };
  var hm = function (min) { var m = Math.round(min); return Math.floor(m / 60) + ' h ' + (m % 60 < 10 ? '0' : '') + (m % 60) + ' min'; };
  var qs = new URLSearchParams(location.search);

  /* -------------------------------------------------- Cost Per Mile */
  if ($('cpmCalc')) {
    TS.tool($('cpmCalc'), {
      validate: function () { return num('cpmLoaded') > num('cpmMiles') ? 'Loaded miles can\'t be more than total miles.' : null; },
      run: function () {
        var fixed = num('cpmPayment') + num('cpmInsurance') + num('cpmPermits') + num('cpmOtherFixed');
        var varMi = num('cpmFuel') + num('cpmMaint') + num('cpmDriverPay');
        var miles = num('cpmMiles'), loaded = num('cpmLoaded');
        var fixedPerMi = fixed / miles, op = fixedPerMi + varMi, ownMi = num('cpmOwner') / miles;
        var allIn = op + ownMi, monthly = allIn * miles;
        $('cpmBig').innerHTML = '$' + allIn.toFixed(2) + '<small>per mile, all-in incl. your pay</small>';
        $('cpmFixedTotal').textContent = money(fixed);
        $('cpmFixedPerMi').textContent = per(fixedPerMi);
        $('cpmVarPerMi').textContent = per(varMi);
        $('cpmOp').textContent = per(op);
        $('cpmOwnerPerMi').textContent = per(ownMi);
        $('cpmLoadedMi').textContent = per(monthly / loaded);
        $('cpmDead').textContent = pctStr((1 - loaded / miles) * 100);
        $('cpmMonthlyTotal').textContent = money(monthly);
        // Hand the all-in CPM (incl. own pay) to the load calculator, so its "profit" is money left after paying yourself.
        var link = $('cpmToLp');
        if (link) { link.href = 'load-profitability-calculator.html?cpm=' + allIn.toFixed(2); link.textContent = 'Check a load with this CPM ($' + allIn.toFixed(2) + ')'; }
      }
    }).run(false);
  }

  /* -------------------------------------------------- Load Profitability (+ compare two loads) */
  if ($('lpCalc')) {
    if (qs.get('cpm') && isFinite(parseFloat(qs.get('cpm')))) $('lpCpm').value = Math.max(0, parseFloat(qs.get('cpm'))).toFixed(2);
    var lpLast = null, loadA = null;
    try { loadA = JSON.parse(sessionStorage.getItem('ts:lpA')); } catch (e) { loadA = null; }
    var lpCompare = function () {
      var box = $('lpCompare');
      $('lpClearA').hidden = !loadA;
      if (!loadA || !lpLast) { box.hidden = true; return; }
      var rows = [
        ['Total revenue', 'rev', money, 1], ['Total trip miles', 'miles', function (x) { return Math.round(x).toLocaleString('en-US') + ' mi'; }, 0],
        ['Driving time', 'hours', function (x) { return x.toFixed(1) + ' h'; }, 0], ['Estimated profit', 'profit', money, 1],
        ['Profit per mile', 'ppm', function (x) { return '$' + x.toFixed(2); }, 1], ['Profit per driving hour', 'pph', function (x) { return money(x); }, 1],
        ['Effective rate', 'eff', function (x) { return '$' + x.toFixed(2) + ' /mi'; }, 1]
      ];
      $('lpCompareRows').innerHTML = rows.map(function (r) {
        var a = loadA[r[1]], b = lpLast[r[1]], better = r[3] ? (b > a ? 'b' : a > b ? 'a' : '') : '';
        return '<tr><th>' + r[0] + '</th><td' + (better === 'a' ? ' class="win"' : '') + '>' + r[2](a) + '</td><td' + (better === 'b' ? ' class="win"' : '') + '>' + r[2](b) + '</td></tr>';
      }).join('');
      box.hidden = false;
    };
    var lp = TS.tool($('lpCalc'), {
      validate: function () {
        var inCpm = $('lpFeesInCpm').checked;
        return !inCpm && num('lpDispatch') + num('lpFactor') >= 100 ? 'Dispatch and factoring fees together must be under 100%.' : null;
      },
      blank: function () { lpLast = null; $('lpCompare').hidden = true; },
      run: function () {
        var L = num('lpRate'), O = num('lpOtherPay'), loaded = num('lpLoaded'), dead = num('lpDeadhead'), ret = num('lpReturn');
        var C = num('lpCpm'), A = num('lpOther'), P = num('lpTarget'), speed = num('lpSpeed');
        var inCpm = $('lpFeesInCpm').checked;
        var d = inCpm ? 0 : num('lpDispatch') / 100, f = inCpm ? 0 : num('lpFactor') / 100;
        var dO = $('lpDispOther').checked ? O : 0, fO = $('lpFactOther').checked ? O : 0;
        var R = L + O, dFee = d * (L + dO), fFee = f * (L + fO);
        var M = loaded + dead + ret, cost = M * C;
        var profit = R - dFee - fFee - cost - A;
        var k = 1 - d - f, adj = d * dO + f * fO;
        var reqL = (cost + A + P - O + adj) / k, beL = (cost + A - O + adj) / k;
        var hours = M / speed;
        $('lpBig').innerHTML = money(profit) + '<small>estimated profit based on entered costs</small>';
        $('lpBig').classList.toggle('neg', profit < 0);
        $('lpRev').textContent = money(R) + (O ? ' (' + money(L) + ' linehaul + ' + money(O) + ' other)' : '');
        $('lpFees').textContent = inCpm ? 'included in your CPM' : money(dFee) + ' / ' + money(fFee);
        $('lpTotalMi').textContent = M.toLocaleString('en-US') + ' mi';
        $('lpTotalCost').textContent = money(cost) + (A ? ' + ' + money(A) + ' extra' : '');
        $('lpMargin').textContent = R > 0 ? pctStr(profit / R * 100) : '-';
        $('lpRatePerLoaded').textContent = per(R / loaded);
        $('lpRatePerTotal').textContent = per(R / M);
        $('lpProfitMi').textContent = (profit < 0 ? '-$' : '$') + Math.abs(profit / M).toFixed(2);
        $('lpHours').textContent = hours.toFixed(1) + ' h at ' + speed + ' mph';
        $('lpBreakEven').textContent = beL <= 0 ? '$0 (other pay covers costs)' : money(beL) + ' (' + per(beL / loaded).replace(' /mi', ' per loaded mi') + ')';
        $('lpRequired').textContent = reqL <= 0 ? '$0 (other pay covers it)' : money(reqL) + ' (' + per(reqL / loaded).replace(' /mi', ' per loaded mi') + ')';
        lpLast = { rev: R, miles: M, hours: hours, profit: profit, ppm: profit / M, pph: profit / hours, eff: R / M };
        lpCompare();
      }
    });
    $('lpSaveA').addEventListener('click', function () {
      if (!lpLast) return;
      loadA = lpLast;
      try { sessionStorage.setItem('ts:lpA', JSON.stringify(loadA)); } catch (e) { /* storage blocked: keep in memory */ }
      TS.track('tool_export', { tool_name: 'load_profit', method: 'compare_save' });
      $('lpSaveA').textContent = 'Replace Load A with this load';
      lpCompare();
    });
    $('lpClearA').addEventListener('click', function () {
      loadA = null; try { sessionStorage.removeItem('ts:lpA'); } catch (e) { /* ignore */ }
      $('lpSaveA').textContent = 'Save as Load A to compare'; lpCompare();
    });
    if (loadA) $('lpSaveA').textContent = 'Replace Load A with this load';
    lp.run(false);
  }

  /* -------------------------------------------------- Break-Even */
  if ($('beCalc')) {
    TS.tool($('beCalc'), {
      run: function () {
        var fixed = num('beFixed'), varMi = num('beVar'), rate = num('beRate'), planned = num('beMiles');
        var contribution = rate - varMi;
        var warn = $('beWarn');
        if (contribution <= 0) {
          warn.style.display = 'block';
          $('beBig').innerHTML = 'No break-even<small>rate does not cover variable cost</small>';
          $('beWeekly').textContent = '-'; $('beMargin').textContent = '$' + contribution.toFixed(2) + ' /mi';
          $('bePlannedProfit').textContent = money((contribution * planned) - fixed);
          return;
        }
        warn.style.display = 'none';
        var beMonthly = fixed / contribution;
        $('beBig').innerHTML = Math.round(beMonthly).toLocaleString('en-US') + '<small>miles / month</small>';
        $('beWeekly').textContent = Math.round(beMonthly / 4.33).toLocaleString('en-US') + ' mi/wk';
        $('beMargin').textContent = '$' + contribution.toFixed(2) + ' /mi';
        $('bePlannedProfit').textContent = money((contribution * planned) - fixed);
      }
    }).run(false);
  }

  /* -------------------------------------------------- Deadhead Miles */
  if ($('dhCalc')) {
    TS.tool($('dhCalc'), {
      positive: ['dhLoaded'],
      run: function () {
        var loaded = num('dhLoaded'), dead = num('dhDead'), rev = num('dhRevenue');
        var total = loaded + dead;
        var quoted = rev / loaded, effective = rev / total;
        $('dhBig').innerHTML = (dead / total * 100).toFixed(1) + '%<small>deadhead miles</small>';
        $('dhTotalMi').textContent = total.toLocaleString('en-US') + ' mi';
        $('dhQuoted').textContent = per(quoted);
        $('dhEffective').textContent = per(effective);
        $('dhLost').textContent = per(Math.max(0, quoted - effective));
        var cpm = num('dhCpm'), row = $('dhProfitRow');
        if (cpm > 0) { row.style.display = ''; $('dhProfit').textContent = money(rev - cpm * total); } else { row.style.display = 'none'; }
      }
    }).run(false);
  }

  /* -------------------------------------------------- Driver Pay */
  if ($('dpCalc')) {
    var dpModel = function () { var c = document.querySelector('input[name=dpModel]:checked'); return c ? c.value : 'mile'; };
    var dpShowGroup = function () {
      var m = dpModel();
      Array.prototype.forEach.call(document.querySelectorAll('#dpCalc .dp-group'), function (gp) { gp.style.display = gp.getAttribute('data-model') === m ? '' : 'none'; });
    };
    Array.prototype.forEach.call(document.querySelectorAll('input[name=dpModel]'), function (r) { r.addEventListener('change', dpShowGroup); });
    dpShowGroup();
    TS.tool($('dpCalc'), {
      positive: ['dpWeeks'], afterRestore: dpShowGroup,
      run: function () {
        dpShowGroup();
        var m = dpModel(), weekly = 0;
        if (m === 'mile') weekly = num('dpRateMile') * num('dpMilesWk');
        else if (m === 'load') weekly = num('dpPayLoad') * num('dpLoadsWk');
        else if (m === 'pct') weekly = num('dpGrossWk') * num('dpPct') / 100;
        else if (m === 'hour') weekly = num('dpHourly') * num('dpHoursWk');
        $('dpBig').innerHTML = money(weekly) + '<small>per week</small>';
        $('dpMonthly').textContent = money(weekly * 4.33);
        $('dpAnnual').textContent = money(weekly * num('dpWeeks'));
      }
    }).run(false);
  }

  /* -------------------------------------------------- IFTA Mileage */
  var ifta = $('iftaCalc');
  if (ifta) {
    var iftaStates = [];
    try { iftaStates = JSON.parse(ifta.getAttribute('data-states')); } catch (e) { iftaStates = ['Texas']; }
    var iftaRows = $('iftaRows');
    var stateOpts = iftaStates.map(function (s) { return '<option>' + s + '</option>'; }).join('');
    var iftaAddRow = function (stateIndex) {
      var tb = document.createElement('tbody');
      tb.innerHTML = '<tr><td><select class="ifta-state" aria-label="State">' + stateOpts + '</select></td>' +
        '<td><input type="number" class="ifta-miles" min="0" step="1" value="0" inputmode="numeric" aria-label="Miles driven"></td>' +
        '<td><input type="number" class="ifta-purchased" min="0" step="1" value="0" inputmode="numeric" aria-label="Gallons purchased"></td>' +
        '<td><input type="number" class="ifta-rate" min="0" step="0.001" placeholder="optional" inputmode="decimal" aria-label="Tax rate paid per gallon"></td>' +
        '<td><button type="button" class="ifta-rm" aria-label="Remove row">&times;</button></td></tr>';
      var row = tb.firstElementChild;
      if (typeof stateIndex === 'number' && row.querySelector('.ifta-state').options[stateIndex]) row.querySelector('.ifta-state').selectedIndex = stateIndex;
      iftaRows.appendChild(row);
    };
    var txIndex = iftaStates.indexOf('Texas');
    iftaAddRow(txIndex >= 0 ? txIndex : 0);
    var iftaTool = TS.tool(ifta, {
      positive: ['iftaMpg'], noSave: true,
      run: function () {
        var mpg = num('iftaMpg');
        var rows = iftaRows.querySelectorAll('tr');
        var totalMiles = 0, totalConsumed = 0, totalPurchased = 0, totalTax = 0, anyRate = false;
        for (var i = 0; i < rows.length; i++) {
          var r = rows[i];
          var miles = parseFloat(r.querySelector('.ifta-miles').value) || 0;
          var purchased = parseFloat(r.querySelector('.ifta-purchased').value) || 0;
          var rate = parseFloat(r.querySelector('.ifta-rate').value) || 0;
          var consumed = miles / mpg;
          totalMiles += miles; totalConsumed += consumed; totalPurchased += purchased;
          if (rate > 0) { anyRate = true; totalTax += (consumed - purchased) * rate; }
        }
        $('iftaTotalMiles').textContent = Math.round(totalMiles).toLocaleString('en-US');
        $('iftaTotalPurchased').textContent = totalPurchased.toFixed(1);
        $('iftaBig').innerHTML = (totalConsumed - totalPurchased).toFixed(1) + '<small>net taxable gallons</small>';
        $('iftaMi').textContent = Math.round(totalMiles).toLocaleString('en-US') + ' mi';
        $('iftaConsumed').textContent = totalConsumed.toFixed(1) + ' gal';
        $('iftaPurchased').textContent = totalPurchased.toFixed(1) + ' gal';
        $('iftaTax').textContent = anyRate ? money(totalTax, 2) : 'Add a rate per row to estimate';
      }
    });
    iftaRows.addEventListener('click', function (e) {
      if (e.target.classList.contains('ifta-rm') && iftaRows.querySelectorAll('tr').length > 1) { e.target.closest('tr').remove(); iftaTool.run(true); }
    });
    $('iftaAddRow').addEventListener('click', function () { iftaAddRow(); iftaTool.run(true); });
    iftaTool.run(false);
  }

  /* -------------------------------------------------- Per Diem */
  if ($('pdCalc')) {
    TS.tool($('pdCalc'), {
      run: function () {
        var total = num('pdDays') * num('pdRate');
        var deductible = total * (num('pdDeductPct') / 100);
        $('pdBig').innerHTML = money(total) + '<small>total per diem, per year</small>';
        $('pdDeductible').textContent = money(deductible);
        $('pdSavings').textContent = money(deductible * (num('pdTaxRate') / 100));
      }
    }).run(false);
  }

  /* -------------------------------------------------- Truck Loan */
  if ($('tlCalc')) {
    TS.tool($('tlCalc'), {
      positive: ['tlTerm'],
      validate: function () { return num('tlDown') > num('tlPrice') ? 'The down payment can\'t be more than the truck price.' : null; },
      run: function () {
        var financed = num('tlPrice') - num('tlDown');
        var n = Math.round(num('tlTerm')), r = (num('tlRate') / 100) / 12;
        var payment = r <= 0 ? financed / n : financed * (r * Math.pow(1 + r, n)) / (Math.pow(1 + r, n) - 1);
        $('tlBig').innerHTML = money(payment, 2) + '<small>per month</small>';
        $('tlFinanced').textContent = money(financed);
        $('tlTotal').textContent = money(payment * n);
        $('tlInterest').textContent = money(Math.max(0, payment * n - financed));
      }
    }).run(false);
  }

  /* -------------------------------------------------- Maintenance Budget */
  if ($('mbCalc')) {
    var mbBracketRate = function (age) { return age <= 2 ? 0.12 : age <= 5 ? 0.18 : age <= 8 ? 0.25 : 0.35; };
    TS.tool($('mbCalc'), {
      run: function () {
        var custom = num('mbCustom'), rate = custom > 0 ? custom : mbBracketRate(num('mbAge'));
        var annual = rate * num('mbMiles');
        $('mbBig').innerHTML = money(annual) + '<small>per year</small>';
        $('mbRate').textContent = '$' + rate.toFixed(2) + ' /mi' + (custom > 0 ? ' (your rate)' : ' (age-based)');
        $('mbMonthly').textContent = money(annual / 12);
        $('mbWeekly').textContent = money(annual / 52);
      }
    }).run(false);
  }

  /* -------------------------------------------------- Hours of Service */
  if ($('hosCalc')) {
    TS.tool($('hosCalc'), {
      run: function () {
        var driven = num('hosDriven'), onDuty = num('hosOnDuty'), elapsed = num('hosElapsed');
        var cycleLimit = parseFloat($('hosCycleType').value) || 70;
        var driveLeft = Math.max(0, 11 - driven);
        var windowLeft = Math.max(0, 14 - elapsed);
        var cycleLeft = Math.max(0, cycleLimit - num('hosCycleUsed') - driven - onDuty);
        var binding = Math.min(driveLeft, windowLeft, cycleLeft);
        var which = 'the 11-hour drive-time limit';
        if (windowLeft === binding && windowLeft <= driveLeft && windowLeft <= cycleLeft) which = 'the 14-hour on-duty window';
        else if (cycleLeft === binding && cycleLeft <= driveLeft && cycleLeft <= windowLeft) which = 'your ' + cycleLimit + '-hour cycle limit';
        $('hosBig').innerHTML = binding.toFixed(1) + '<small>more hours today</small>';
        $('hosDriveLeft').textContent = driveLeft.toFixed(1) + ' hr';
        $('hosWindowLeft').textContent = windowLeft.toFixed(1) + ' hr';
        $('hosCycleLeft').textContent = cycleLeft.toFixed(1) + ' hr';
        $('hosBinding').textContent = binding <= 0 ? 'None left: go off duty' : which;
      }
    }).run(false);
  }

  /* -------------------------------------------------- Freight Class */
  if ($('fcCalc')) {
    var fcClassFor = function (pcf) {
      var t = [[50, '50'], [35, '55'], [30, '60'], [22.5, '65'], [15, '70'], [12, '77.5'], [10, '85'], [8, '92.5'], [6, '100'], [4, '125'], [2, '150'], [1, '175']];
      for (var i = 0; i < t.length; i++) if (pcf >= t[i][0]) return t[i][1];
      return '250+';
    };
    TS.tool($('fcCalc'), {
      positive: ['fcL', 'fcW', 'fcH', 'fcWeight', 'fcUnits'],
      run: function () {
        var units = Math.round(num('fcUnits'));
        var totalCube = num('fcL') * num('fcW') * num('fcH') / 1728 * units;
        var totalWeight = num('fcWeight') * units;
        var density = totalWeight / totalCube;
        $('fcClass').textContent = 'Class ' + fcClassFor(density);
        $('fcDensity').textContent = density.toFixed(1) + ' lb/ft³';
        $('fcCube').textContent = totalCube.toFixed(1) + ' ft³';
        $('fcTotalWeight').textContent = totalWeight.toLocaleString('en-US') + ' lbs';
      },
      blank: function () { $('fcClass').textContent = '-'; }
    }).run(false);
  }

  /* -------------------------------------------------- Fuel Surcharge */
  var fsc = $('fscCalc');
  if (fsc) {
    var FS = {};
    try { FS = JSON.parse(fsc.getAttribute('data-fuel')); } catch (e) { FS = {}; }
    var us = FS.us;
    if (us && us.price) {
      us.status = TS.fuelStatus(us.observed, 'weekly', FS.maxAge);
      $('fscCurrent').value = us.price.toFixed(3);
      $('fscCurrentNote').textContent = 'Filled in: ' + TS.fuelLabel(us) + ', $' + us.price.toFixed(3) + '/gal (U.S. average). Type the index price your contract names.';
      if (us.status === 'stale') $('fscCurrentNote').className = 'hint stale';
    } else {
      $('fscCurrentNote').textContent = 'No current EIA average available. Type the index price your contract names.';
    }
    var method = function () { return $('fscMethod').value; };
    var showMethod = function () {
      Array.prototype.forEach.call(fsc.querySelectorAll('.fsc-m'), function (el) { el.hidden = el.getAttribute('data-m').split(' ').indexOf(method()) < 0; });
    };
    $('fscMethod').addEventListener('change', showMethod);
    showMethod();
    TS.tool(fsc, {
      afterRestore: showMethod,
      validate: function () { return method() === 'steppct' && !(num('fscLinehaul') > 0) ? 'Enter your linehaul rate per mile: the % method is a share of linehaul.' : null; },
      run: function () {
        showMethod();
        var m = method(), diff = num('fscCurrent') - num('fscBase'), lh = num('fscLinehaul');
        var d = diff < 0 && $('fscBelow').value === 'zero' ? 0 : diff;
        var steps = null, perMile, pct = null;
        if (m === 'mpg') perMile = d / num('fscMpg');
        else {
          var raw = Math.abs(d) / num('fscStep');
          steps = ($('fscRound').value === 'up' ? Math.ceil(raw - 1e-9) : Math.floor(raw + 1e-9)) * (d < 0 ? -1 : 1);
          if (m === 'stepcpm') perMile = steps * num('fscCents') / 100;
          else { pct = steps * num('fscPctStep'); perMile = lh * pct / 100; }
        }
        if (pct === null && lh > 0) pct = perMile / lh * 100;
        var total = perMile * num('fscMiles');
        $('fscBig').innerHTML = money(total, 2) + '<small>' + (perMile < 0 ? 'credit' : 'surcharge') + ' for ' + num('fscMiles').toLocaleString('en-US') + ' miles</small>';
        $('fscDiff').textContent = (diff < 0 ? '-$' : '$') + Math.abs(diff).toFixed(3) + ' /gal';
        $('fscSteps').textContent = steps === null ? 'not used' : String(steps);
        $('fscPerMile').textContent = (perMile < 0 ? '-$' : '$') + Math.abs(perMile).toFixed(3) + ' /mi';
        $('fscPct').textContent = pct === null ? 'add a linehaul rate' : pctStr(pct);
        $('fscTotal').textContent = money(total, 2);
      }
    }).run(false);
  }

  /* -------------------------------------------------- Detention Pay */
  var det = $('detCalc');
  if (det) {
    var pad = function (n) { return (n < 10 ? '0' : '') + n; };
    var localIso = function (d, h, m) { return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate()) + 'T' + pad(h) + ':' + pad(m); };
    var today = new Date();
    if (!$('detArrive').value) { $('detAppt').value = localIso(today, 8, 0); $('detArrive').value = localIso(today, 8, 0); $('detRelease').value = localIso(today, 13, 10); }
    var t = function (id) { var v = $(id).value; return v ? new Date(v).getTime() : null; };
    var clock = function (ms) { return new Date(ms).toLocaleString([], { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' }); };
    TS.tool(det, {
      validate: function () { return t('detRelease') !== null && t('detArrive') !== null && t('detRelease') <= t('detArrive') ? 'The release time must be after the arrival time.' : null; },
      run: function () {
        var arrive = t('detArrive'), release = t('detRelease'), appt = t('detAppt');
        var start = arrive, warn = '';
        if (appt !== null && arrive < appt) { start = appt; warn = 'You arrived before the appointment, so the clock starts at the appointment time.'; }
        if (appt !== null && arrive > appt) warn = 'You arrived after the appointment. Many agreements do not pay detention for a late arrival; check yours.';
        var onSite = (release - arrive) / 60000;
        var eligible = Math.max(0, (release - start) / 60000 - num('detFree') * 60);
        var inc = parseInt($('detInc').value, 10), units = eligible / inc, rnd = $('detRound').value;
        var billMin = (rnd === 'up' ? Math.ceil(units - 1e-9) : rnd === 'near' ? Math.round(units) : Math.floor(units + 1e-9)) * inc;
        var cap = num('detCap');
        if (cap > 0) billMin = Math.min(billMin, cap * 60);
        var pay = billMin / 60 * num('detRate');
        $('detBig').innerHTML = money(pay, 2) + '<small>estimated detention pay</small>';
        $('detStart').textContent = clock(start);
        $('detOnSite').textContent = hm(onSite);
        $('detEligible').textContent = hm(eligible);
        $('detBillable').textContent = (billMin / 60).toFixed(2) + ' h' + (cap > 0 && billMin === cap * 60 ? ' (capped)' : '');
        $('detWarn').textContent = warn; $('detWarn').hidden = !warn;
      },
      blank: function () { $('detWarn').hidden = true; }
    }).run(false);
  }
})();
