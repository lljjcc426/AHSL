# F1 runtime resource audit

Audit time: 2026-10-02 22:44 CST (UTC+08:00)

## Host resources

- Logical CPUs: 20
- RAM: 31.6 GiB
- Ubuntu VHDX location: `C:\Users\cc\AppData\Local\wsl\{ea43aa54-76b9-435e-bd5d-dc990288f070}\ext4.vhdx`
- Ubuntu VHDX current file size: 14.14 GiB
- Governing host drive free space: 55.6 GiB
- Storage class: STORAGE-C

## WSL resources

The Ubuntu WSL2 VM could not start during this audit. Consequently, current `nproc`, `free -h`, `df -h`, and `df -T` measurements are unavailable and are not inferred from an earlier session.

No `.wslconfig` resource tuning is recommended at this checkpoint. Restoring the required Windows virtualization component is the first action; resource tuning would be premature.

