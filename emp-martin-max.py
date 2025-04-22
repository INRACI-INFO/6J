"""
    name : martin stordeur && maxime kapczuk 
    date : 2023-10-05
    description : Application de lecture d'empreintes digitales utilisan.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import ctypes
import ctypes.wintypes as wintypes
import sys

WINBIO_SESSION_HANDLE = wintypes.ULONG
WINBIO_UNIT_ID = wintypes.ULONG
WINBIO_REJECT_DETAIL = wintypes.ULONG
HRESULT = ctypes.c_long
PBYTE = ctypes.POINTER(wintypes.BYTE)
SIZE_T = ctypes.c_size_t
PVOID = ctypes.c_void_p

WINBIO_TYPE_FINGERPRINT = 0x00000008
WINBIO_POOL_SYSTEM = 0x00000001
WINBIO_OPEN_FLAG_DEFAULT = 0x00000000
WINBIO_FLAG_PROCESSED = 0x00000002
WINBIO_ASYNC_NOTIFY_CALLBACK = 0x00000001
WINBIO_STATE_ACCEPT = 0x01
WINBIO_STATE_REJECT = 0x02
WINBIO_STATE_NO_CONTACT = 0x03
WINBIO_STATE_BAD_READ = 0x04
WINBIO_STATE_DIRTY = 0x05
WINBIO_STATE_UNKNOWN = 0x00

class GUID(ctypes.Structure):
    _fields_ = [
        ("Data1", wintypes.ULONG),
        ("Data2", wintypes.USHORT),
        ("Data3", wintypes.USHORT),
        ("Data4", ctypes.c_ubyte * 8)
    ]

class WINBIO_IDENTITY(ctypes.Structure):
     _fields_ = [
         ("Type", wintypes.ULONG),
         ("Value", ctypes.c_ubyte * 48)
     ]

class WINBIO_ASYNC_IDENTIFY_RESULT(ctypes.Structure):
    _fields_ = [
        ("Identity", WINBIO_IDENTITY),
        ("SubFactor", wintypes.ULONG),
        ("RejectDetail", WINBIO_REJECT_DETAIL),
    ]

class WINBIO_ASYNC_CAPTURE_RESULT(ctypes.Structure):
     _fields_ = [
         ("Sample", PVOID),
         ("SampleSize", SIZE_T),
         ("RejectDetail", WINBIO_REJECT_DETAIL),
     ]

class WINBIO_ASYNC_ENROLL_RESULT(ctypes.Structure):
    _fields_ = [
        ("OperationStatus", wintypes.ULONG),
        ("RejectDetail", WINBIO_REJECT_DETAIL),
    ]

class _WINBIO_ASYNC_RESULT_UNION(ctypes.Union):
    _fields_ = [
        ("Identify", WINBIO_ASYNC_IDENTIFY_RESULT),
        ("Capture", WINBIO_ASYNC_CAPTURE_RESULT),
        ("Enroll", WINBIO_ASYNC_ENROLL_RESULT),
    ]

class WINBIO_ASYNC_RESULT(ctypes.Structure):
    _fields_ = [
        ("SessionHandle", WINBIO_SESSION_HANDLE),
        ("Operation", wintypes.ULONG),
        ("Status", HRESULT),
        ("UnitId", WINBIO_UNIT_ID),
        ("ParametersOrResults", _WINBIO_ASYNC_RESULT_UNION),
    ]

WINBIO_OPERATION_ENROLL_CAPTURE = 0
WINBIO_OPERATION_ENROLL_COMMIT = 1
WINBIO_OPERATION_IDENTIFY = 2

class WINBIO_UNIT_SCHEMA(ctypes.Structure):
    _fields_ = [
        ("UnitId", WINBIO_UNIT_ID),
        ("PoolType", wintypes.ULONG),
        ("BiometricUnitType", wintypes.ULONG),
        ("BiometricUnitSubType", wintypes.ULONG),
        ("DeviceInstanceId", GUID),
        ("StorageId", GUID),
        ("Capabilities", ctypes.c_ulonglong),
        ("UnitStatus", wintypes.DWORD),
        ("Description", wintypes.LPWSTR)
    ]

WINBIO_ASYNC_RESULT_CALLBACK = ctypes.WINFUNCTYPE(
    None,
    PVOID,
    ctypes.POINTER(WINBIO_ASYNC_RESULT)
)

try:
    winbio = ctypes.WinDLL('Winbio.dll')
except OSError as e:
    print(f"Erreur: Impossible de charger Winbio.dll. Assurez-vous que la DLL est accessible.")
    print(e)
    sys.exit()

winbio.WinBioAsyncOpenSession.argtypes = [
    wintypes.ULONG, wintypes.ULONG, wintypes.ULONG,
    ctypes.POINTER(WINBIO_UNIT_ID), SIZE_T,
    ctypes.POINTER(GUID),
    wintypes.ULONG, WINBIO_ASYNC_RESULT_CALLBACK, PVOID,
    ctypes.POINTER(WINBIO_SESSION_HANDLE)
]
winbio.WinBioAsyncOpenSession.restype = HRESULT

winbio.WinBioCloseSession.argtypes = [WINBIO_SESSION_HANDLE]
winbio.WinBioCloseSession.restype = HRESULT

winbio.WinBioFree.argtypes = [PVOID]
winbio.WinBioFree.restype = HRESULT

winbio.WinBioEnrollBegin.argtypes = [
    WINBIO_SESSION_HANDLE, wintypes.ULONG,
    ctypes.POINTER(WINBIO_UNIT_ID),
    ctypes.POINTER(WINBIO_REJECT_DETAIL)
]
winbio.WinBioEnrollBegin.restype = HRESULT

winbio.WinBioAsyncEnrollCapture.argtypes = [
    WINBIO_SESSION_HANDLE, wintypes.ULONG
]
winbio.WinBioAsyncEnrollCapture.restype = HRESULT

winbio.WinBioAsyncEnrollCommit.argtypes = [
    WINBIO_SESSION_HANDLE,
    ctypes.POINTER(WINBIO_IDENTITY),
    PVOID, SIZE_T
]
winbio.WinBioAsyncEnrollCommit.restype = HRESULT

winbio.WinBioAsyncIdentify.argtypes = [
    WINBIO_SESSION_HANDLE,
    ctypes.POINTER(WINBIO_UNIT_ID)
]
winbio.WinBioAsyncIdentify.restype = HRESULT

winbio.WinBioCancel.argtypes = [WINBIO_SESSION_HANDLE]
winbio.WinBioCancel.restype = HRESULT

winbio.WinBioEnumBiometricUnits.argtypes = [
    wintypes.ULONG,
    ctypes.POINTER(ctypes.POINTER(WINBIO_UNIT_SCHEMA)),
    ctypes.POINTER(SIZE_T)
]
winbio.WinBioEnumBiometricUnits.restype = HRESULT

class BiometricApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interface biométrique (WBF)")
        self.session_handle = WINBIO_SESSION_HANDLE()
        self.wbf_opened = False
        self.enroll_state = 0

        self.callback_context = ctypes.cast(ctypes.pointer(ctypes.py_object(self)), PVOID)
        self._enroll_callback = WINBIO_ASYNC_RESULT_CALLBACK(self.enroll_callback)
        self._identify_callback = WINBIO_ASYNC_RESULT_CALLBACK(self.identify_callback)

        self.setup_gui()
        self.open_wbf_session_async()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_gui(self):
        self.tab_control = ttk.Notebook(self.root)

        self.tab_enregistrer = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_enregistrer, text=' Enregistrement ')

        ttk.Label(self.tab_enregistrer, text="Nom d'utilisateur (pour référence):").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.reg_username_entry = ttk.Entry(self.tab_enregistrer)
        self.reg_username_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        self.btn_enregistrer = ttk.Button(self.tab_enregistrer, text="Commencer l'enregistrement", command=self.start_enrollment)
        self.btn_enregistrer.grid(row=1, column=0, columnspan=2, padx=5, pady=10)

        self.reg_status_label = ttk.Label(self.tab_enregistrer, text="Statut : Inactif")
        self.reg_status_label.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky='w')

        self.tab_connecter = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_connecter, text=' Connexion ')

        ttk.Label(self.tab_connecter, text="Nom d'utilisateur (pour référence):").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.login_username_entry = ttk.Entry(self.tab_connecter)
        self.login_username_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        self.btn_connecter = ttk.Button(self.tab_connecter, text="Connecter avec empreinte", command=self.start_identification)
        self.btn_connecter.grid(row=1, column=0, columnspan=2, padx=5, pady=10)

        self.login_status_label = ttk.Label(self.tab_connecter, text="Statut : Inactif")
        self.login_status_label.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky='w')

        self.tab_control.pack(expand=1, fill="both", padx=10, pady=10)

    def open_wbf_session_async(self, for_enrollment=False):
        if self.wbf_opened:
            return

        async_session_handle = WINBIO_SESSION_HANDLE()
        callback_func = self._enroll_callback if for_enrollment else self._identify_callback

        hr = winbio.WinBioAsyncOpenSession(
            WINBIO_TYPE_FINGERPRINT,
            WINBIO_POOL_SYSTEM,
            WINBIO_OPEN_FLAG_DEFAULT,
            None, 0, None,
            WINBIO_ASYNC_NOTIFY_CALLBACK,
            callback_func,
            self.callback_context,
            ctypes.byref(async_session_handle)
        )

        if hr < 0:
            error_msg = f"Erreur WinBioAsyncOpenSession: HRESULT=0x{hr & 0xFFFFFFFF:08X}"
            try:
                error_msg += f"\n  Message d'erreur: {ctypes.FormatError(hr).strip()}"
            except:
                pass
            messagebox.showerror("Erreur WBF", error_msg)
            self.wbf_opened = False
            self.reg_status_label.config(text=f"Statut : {error_msg}")
            self.login_status_label.config(text=f"Statut : {error_msg}")
            self.btn_enregistrer.config(state=tk.DISABLED)
            self.btn_connecter.config(state=tk.DISABLED)
        else:
            self.session_handle = async_session_handle
            self.wbf_opened = True
            status_text = "Session WBF asynchrone ouverte."
            self.reg_status_label.config(text=f"Statut : {status_text}")
            self.login_status_label.config(text=f"Statut : {status_text}")
            print(f"Session WBF asynchrone ouverte (Handle: {self.session_handle.value}).")

            self.enumerate_units()

            if for_enrollment:
                self.start_async_enrollment_sequence()


    def close_wbf_session(self):
        if self.wbf_opened and self.session_handle.value:
            winbio.WinBioCancel(self.session_handle)
            hr = winbio.WinBioCloseSession(self.session_handle)
            if hr < 0:
                 print(f"Attention: Erreur WinBioCloseSession: HRESULT=0x{hr & 0xFFFFFFFF:08X}")
                 try:
                    print(f"  Message d'erreur: {ctypes.FormatError(hr).strip()}")
                 except:
                    pass
            print("Session WBF fermée.")
            self.wbf_opened = False
            self.session_handle = WINBIO_SESSION_HANDLE()

    def on_closing(self):
        self.close_wbf_session()
        self.root.destroy()

    def enumerate_units(self):
        if not self.wbf_opened:
            print("Énumération impossible : session WBF non ouverte.")
            return

        unit_schema_array = ctypes.POINTER(WINBIO_UNIT_SCHEMA)()
        unit_count = SIZE_T()

        print("--- Énumération des unités biométriques (Type Empreinte Digitale) ---")

        hr = winbio.WinBioEnumBiometricUnits(
            WINBIO_TYPE_FINGERPRINT,
            ctypes.byref(unit_schema_array),
            ctypes.byref(unit_count)
        )

        if hr < 0:
            print(f"Erreur WinBioEnumBiometricUnits: HRESULT=0x{hr & 0xFFFFFFFF:08X}")
            try:
                print(f"  Message d'erreur: {ctypes.FormatError(hr).strip()}")
            except:
                pass
            print("--- Fin de l'énumération ---")
            return

        print(f"Unités trouvées: {unit_count.value}")
        if unit_count.value > 0 and unit_schema_array:
            for i in range(unit_count.value):
                unit = unit_schema_array[i]
                print(f"  Unité {i+1}:")
                print(f"    ID: {unit.UnitId}")
                print(f"    Pool: {unit.PoolType}")
                print(f"    Type: {unit.BiometricUnitType}")
                print(f"    Sous-type: {unit.BiometricUnitSubType}")
                print(f"    Statut: {unit.UnitStatus}")
                print(f"    Description: {unit.Description}")

            winbio.WinBioFree(unit_schema_array)
            print("Mémoire de l'énumération libérée.")
        else:
            print("Aucune unité d'empreinte digitale trouvée.")

        print("--- Fin de l'énumération ---")


    def enroll_callback(self, pvContext, pAsyncResult):
        app_instance = ctypes.cast(pvContext, ctypes.POINTER(ctypes.py_object)).contents.value
        result = pAsyncResult.contents
        hr = result.Status

        if hr < 0:
             error_msg = f"Erreur Opération Enrôlement: HRESULT=0x{hr & 0xFFFFFFFF:08X}"
             try:
                 error_msg += f"\n  Message d'erreur: {ctypes.FormatError(hr).strip()}"
             except:
                 pass
             print(error_msg)
             app_instance.root.after(0, app_instance.update_enroll_status, f"Statut : Échec de l'enregistrement. {error_msg}", True)
             winbio.WinBioCancel(app_instance.session_handle)
             return

        if result.Operation == 0:
             enroll_result = result.ParametersOrResults.Enroll
             operation_state = enroll_result.OperationStatus
             reject_detail = enroll_result.RejectDetail

             print(f"Capture Enrôlement async reçue (Statut Op: {operation_state}, Rejet: {reject_detail})")

             if operation_state == WINBIO_STATE_ACCEPT:
                 app_instance.root.after(0, app_instance.update_enroll_status, "Statut : Capture acceptée. Placez votre doigt à nouveau...", False)
                 app_instance.root.after(100, app_instance.initiate_async_enroll_capture)
             elif operation_state == WINBIO_STATE_REJECT:
                 app_instance.root.after(0, app_instance.update_enroll_status, f"Statut : Capture rejetée (Code: {reject_detail}). Réessayez...", False)
                 app_instance.root.after(100, app_instance.initiate_async_enroll_capture)
             elif operation_state == WINBIO_STATE_NO_CONTACT or operation_state == WINBIO_STATE_BAD_READ:
                  app_instance.root.after(0, app_instance.update_enroll_status, f"Statut : Mauvaise lecture (Code: {operation_state}). Réessayez...", False)
                  app_instance.root.after(100, app_instance.initiate_async_enroll_capture)
             elif operation_state == WINBIO_STATE_UNKNOWN:
                 app_instance.root.after(0, app_instance.update_enroll_status, "Statut : Enrôlement potentiellement terminé. Tentative de validation...", False)
                 app_instance.root.after(100, app_instance.commit_async_enrollment)
             else:
                 app_instance.root.after(0, app_instance.update_enroll_status, f"Statut : État d'opération inconnu ({operation_state}).", True)

        elif result.Operation == 1:
            if hr >= 0:
                 print("WinBioAsyncEnrollCommit réussi.")
                 app_instance.root.after(0, app_instance.update_enroll_status, "Statut : Enregistrement terminé avec succès !", True)
            else:
                 print(f"WinBioAsyncEnrollCommit échec: HRESULT=0x{hr & 0xFFFFFFFF:08X}")
                 try:
                     print(f"  Message d'erreur: {ctypes.FormatError(hr).strip()}")
                 except:
                     pass
                 app_instance.root.after(0, app_instance.update_enroll_status, f"Statut : Échec de la validation. Code: 0x{hr & 0xFFFFFFFF:08X}", True)
                 winbio.WinBioCancel(app_instance.session_handle)

        else:
             print(f"Callback Enrôlement: Opération inconnue reçue: {result.Operation}")
             app_instance.root.after(0, app_instance.update_enroll_status, f"Statut : Opération Enrôlement inconnue ({result.Operation}).", True)


    def identify_callback(self, pvContext, pAsyncResult):
        app_instance = ctypes.cast(pvContext, ctypes.POINTER(ctypes.py_object)).contents.value
        result = pAsyncResult.contents
        hr = result.Status

        if hr < 0:
            error_msg = f"Erreur Opération Identification: HRESULT=0x{hr & 0xFFFFFFFF:08X}"
            try:
                error_msg += f"\n  Message d'erreur: {ctypes.FormatError(hr).strip()}"
            except:
                pass
            print(error_msg)
            app_instance.root.after(0, app_instance.update_login_status, f"Statut : Échec de l'identification. {error_msg}", True)
            return

        if result.Operation == 2:
            identify_result = result.ParametersOrResults.Identify

            print(f"Identification async reçue (Unité: {result.UnitId}, Rejet: {identify_result.RejectDetail})")

            if hr >= 0:
                 print(f"Identification réussie sur l'unité {result.UnitId}!")
                 app_instance.root.after(0, app_instance.update_login_status, "Statut : Identification réussie. Accès accordé !", True)
            else:
                 print(f"Identification échouée. HRESULT: 0x{hr & 0xFFFFFFFF:08X}")
                 app_instance.root.after(0, app_instance.update_login_status, "Statut : Identification échouée. Accès refusé.", True)

        else:
             print(f"Callback Identification: Opération inconnue reçue: {result.Operation}")
             app_instance.root.after(0, app_instance.update_login_status, f"Statut : Opération Identification inconnue ({result.Operation}).", True)


    def update_enroll_status(self, text, enable_button=False):
        self.reg_status_label.config(text=text)
        if enable_button:
            self.btn_enregistrer.config(state=tk.NORMAL)
            self.enroll_state = 0
        else:
            self.btn_enregistrer.config(state=tk.DISABLED)

    def update_login_status(self, text, enable_button=False):
        self.login_status_label.config(text=text)
        if enable_button:
            self.btn_connecter.config(state=tk.NORMAL)
        else:
            self.btn_connecter.config(state=tk.DISABLED)

    def start_enrollment(self):
        if not self.wbf_opened:
            messagebox.showwarning("Attention", "Session WBF non ouverte.")
            self.open_wbf_session_async(for_enrollment=True)
            return

        self.close_wbf_session()
        self.open_wbf_session_async(for_enrollment=True)


    def start_async_enrollment_sequence(self):
        if not self.wbf_opened: return

        self.update_enroll_status("Statut : Démarrage de l'enregistrement async...", False)
        self.enroll_state = 1

        reject_detail = WINBIO_REJECT_DETAIL()
        hr = winbio.WinBioEnrollBegin(
            self.session_handle,
            WINBIO_TYPE_FINGERPRINT,
            None,
            ctypes.byref(reject_detail)
        )

        if hr < 0:
            error_msg = f"Erreur WinBioEnrollBegin (setup async): HRESULT=0x{hr & 0xFFFFFFFF:08X}"
            try:
                 error_msg += f"\n  Message d'erreur: {ctypes.FormatError(hr).strip()}"
            except:
                 pass
            print(error_msg)
            self.update_enroll_status(f"Statut : {error_msg}", True)
            winbio.WinBioCancel(self.session_handle)
            return

        print("WinBioEnrollBegin (setup async) réussi. Prêt pour les captures async.")
        self.update_enroll_status("Statut : Placez votre doigt sur le lecteur...", False)
        self.enroll_state = 2

        self.initiate_async_enroll_capture()


    def initiate_async_enroll_capture(self):
        if not self.wbf_opened or self.enroll_state != 2:
             return

        hr = winbio.WinBioAsyncEnrollCapture(
            self.session_handle,
            WINBIO_FLAG_PROCESSED
        )

        if hr < 0:
            error_msg = f"Erreur WinBioAsyncEnrollCapture: HRESULT=0x{hr & 0xFFFFFFFF:08X}"
            try:
                 error_msg += f"\n  Message d'erreur: {ctypes.FormatError(hr).strip()}"
            except:
                 pass
            print(error_msg)
            self.update_enroll_status(f"Statut : {error_msg}", True)
            winbio.WinBioCancel(self.session_handle)


    def commit_async_enrollment(self):
        if not self.wbf_opened: return

        self.update_enroll_status("Statut : Validation de l'enregistrement async...", False)

        hr = winbio.WinBioAsyncEnrollCommit(
            self.session_handle,
            None,
            None,
            0
        )

        if hr < 0:
             error_msg = f"Erreur WinBioAsyncEnrollCommit: HRESULT=0x{hr & 0xFFFFFFFF:08X}"
             try:
                 error_msg += f"\n  Message d'erreur: {ctypes.FormatError(hr).strip()}"
             except:
                 pass
             print(error_msg)
             self.update_enroll_status(f"Statut : Échec de la validation async. {error_msg}", True)
             winbio.WinBioCancel(self.session_handle)


    def start_identification(self):
        if not self.wbf_opened:
            messagebox.showwarning("Attention", "Session WBF non ouverte.")
            self.open_wbf_session_async(for_enrollment=False)
            return

        self.close_wbf_session()
        self.open_wbf_session_async(for_enrollment=False)

    def start_async_identification(self):
        if not self.wbf_opened: return

        self.update_login_status("Statut : Démarrage de l'identification async...", False)

        hr = winbio.WinBioAsyncIdentify(
            self.session_handle,
            None
        )

        if hr < 0:
             error_msg = f"Erreur WinBioAsyncIdentify: HRESULT=0x{hr & 0xFFFFFFFF:08X}"
             try:
                 error_msg += f"\n  Message d'erreur: {ctypes.FormatError(hr).strip()}"
             except:
                 pass
             print(error_msg)
             self.update_login_status(f"Statut : {error_msg}", True)
             winbio.WinBioCancel(self.session_handle)


if __name__ == "__main__":
    root = tk.Tk()
    app = BiometricApp(root)
    root.mainloop()