use solana_program::{
    account_info::AccountInfo, entrypoint, entrypoint::ProgramResult, msg,
    program_error::ProgramError, pubkey::Pubkey,
};

entrypoint!(_entry);
fn _entry(_program_id: &Pubkey, _accounts: &[AccountInfo], data: &[u8]) -> ProgramResult {
    let log = match String::from_utf8(data.to_vec()) {
        Ok(log) => log,
        Err(_) => return Err(ProgramError::InvalidInstructionData),
    };
    msg!("Evidence URI: {}", log);
    Ok(())
}
