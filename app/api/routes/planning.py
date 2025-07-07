from fastapi import APIRouter, HTTPException, status
from app.services.ai_planning_service import aiPlanningService
from app.schemas.requete import GeneratePlanningRequest
from app.schemas.response import PlanningResponse, StatusResponse
from app.services.database_service import databaseService

# Router avec préfixe et tags
router = APIRouter(
    prefix="/api/planning",
    tags=["AI Planning"]
)


@router.post("/generate", response_model=PlanningResponse, status_code=status.HTTP_201_CREATED)
async def generate_planning(request: GeneratePlanningRequest):
    """Génère un planning IA pour un tournoi"""
    try:
        # Appel du service AI Planning
        planning = aiPlanningService.generatePlanning(request.tournament_id)
        
        if not planning:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Impossible de générer le planning. Vérifiez les données du tournoi."
            )
        
        return PlanningResponse(
            success=True,
            message="Planning généré avec succès",
            data=planning
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erreur génération planning: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne lors de la génération du planning"
        )

@router.get("/{planning_id}/status", response_model=StatusResponse)
async def get_planning_status(planning_id: str):
    """Récupère le statut d'un planning"""
    try:
        # Appel du service
        status_value = aiPlanningService.getPlanningStatus(planning_id)
        
        if status_value is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Planning non trouvé"
            )
        
        return StatusResponse(
            success=True,
            message="Statut récupéré avec succès",
            data={"status": status_value, "planning_id": planning_id}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erreur récupération statut: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne lors de la récupération du statut"
        )

@router.post("/{planning_id}/regenerate", response_model=PlanningResponse)
async def regenerate_planning(planning_id: str):
    """Régénère un planning existant"""
    try:
        # Appel du service
        new_planning = aiPlanningService.regeneratePlanning(planning_id)
        
        if not new_planning:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Planning original non trouvé ou erreur lors de la régénération"
            )
        
        return PlanningResponse(
            success=True,
            message="Planning régénéré avec succès",
            data=new_planning
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erreur régénération planning: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne lors de la régénération du planning"
        )

@router.get("/{planning_id}", response_model=PlanningResponse)
async def get_planning_by_id(planning_id: str):
    """Récupère un planning complet par son ID"""
    try:        
        planning_details = databaseService.getPlanningWithDetailsByPlanningId(planning_id)
        
        if not planning_details:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Planning non trouvé"
            )
        
        return PlanningResponse(
            success= True,
            message= "Planning récupéré avec succès",
            data= planning_details
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erreur récupération planning: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne lors de la récupération du planning"
        )
    
@router.get("/tournament/{tournament_id}", response_model=PlanningResponse)
async def get_planning_by_tournament_id(tournament_id: str):
    """Récupère un planning complet par l'ID du tournoi"""
    try:
        # Appel du service
        planning_details = databaseService.getPlanningWithDetailsByTournamentId(tournament_id)
        
        if not planning_details:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Planning non trouvé"
            )
        
        return PlanningResponse(
            success=True,
            message="Planning récupéré avec succès",
            data=planning_details
        )
    except Exception as e:
        print(f"❌ Erreur récupération planning: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne lors de la récupération du planning"
        )